from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.services.audit import record


from .models import IdentityProfile, VerificationRequest, EmailVerificationToken, VerifiableCredential
from .serializers import (
    RegisterSerializer,
    IdentityProfileSerializer,
    VerificationRequestSerializer,
)

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')
class ThrottledTokenObtainPairView(TokenObtainPairView):
    """Login endpoint, rate-limited by IP to slow down credential-stuffing/brute-force attempts."""
    pass

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # If a previous registration with this username/email was never verified,
        # remove the stale, unverified account so the person can register again
        # instead of being permanently blocked by a "already exists" error.
        username = (request.data.get('username') or '').strip()
        email = (request.data.get('email') or '').strip().lower()

        if username or email:
            User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=email),
                is_active=False,
            ).delete()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.is_active = False
        user.save(update_fields=['is_active'])

        verification = EmailVerificationToken.objects.create(user=user)

        verification_url = (
            f"{settings.FRONTEND_URL}/verify-email/{verification.token}/"
        )

        send_mail(
            subject='Verify your JVCP account',
            message=(
                f'Welcome to JVCP, {user.username}.\n\n'
                f'Click the link below to verify your email:\n\n'
                f'{verification_url}\n\n'
                f'If you did not create this account, ignore this email.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({
            'detail': 'Account created. Please check your email to verify your account.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
        }, status=status.HTTP_201_CREATED)


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = IdentityProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = IdentityProfile.objects.get_or_create(user=self.request.user)
        return profile


class SubmitVerificationView(generics.CreateAPIView):
    serializer_class = VerificationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile, _ = IdentityProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class GoogleLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        credential = request.data.get('credential')

        if not credential:
            return Response(
                {'detail': 'Google credential is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            google_user = id_token.verify_oauth2_token(
                credential,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            return Response(
                {'detail': 'Invalid Google credential.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        email = google_user.get('email')
        name = google_user.get('name', '')

        if not email:
            return Response(
                {'detail': 'Google account has no email.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': name,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        try:
            verification = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {'detail': 'Invalid verification link.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = verification.user
        user.is_active = True
        user.save(update_fields=['is_active'])

        profile, _ = IdentityProfile.objects.get_or_create(user=user)
        profile.is_verified = True
        profile.save(update_fields=['is_verified'])

        verification.delete()

        refresh = RefreshToken.for_user(user)

        return Response({
            'detail': 'Email verified successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class VerifyCredentialView(APIView):
    """Public credential-verification endpoint — any relying party can check a credential's
    validity without authenticating, same as checking a real DID/VC would work."""
    permission_classes = [permissions.AllowAny]

    def get(self, request, credential_id):
        try:
            vc = VerifiableCredential.objects.get(credential_id=credential_id)
        except VerifiableCredential.DoesNotExist:
            return Response({"valid": False, "reason": "not_found"}, status=404)

        expired = bool(vc.expires_at and vc.expires_at < timezone.now())
        valid = not vc.revoked and not expired

        return Response({
            "valid": valid,
            "revoked": vc.revoked,
            "expired": expired,
            "issuer_did": vc.issuer_did,
            "subject_did": vc.subject_did,
            "claims": vc.claims,
            "issued_at": vc.issued_at,
            "expires_at": vc.expires_at,
            "note": "Mock W3C-style credential — prototype only, not a production DID/VC implementation.",
        })


class RevokeCredentialView(APIView):
    """Admin-only revocation."""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, credential_id):
        try:
            vc = VerifiableCredential.objects.get(credential_id=credential_id)
        except VerifiableCredential.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        vc.revoked = True
        vc.save()
        record('VC_REVOKED', request.user, 'VerifiableCredential', vc.credential_id)
        return Response({"credential_id": str(vc.credential_id), "revoked": True})