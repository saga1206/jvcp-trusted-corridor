from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import dns.resolver

from .models import (
    IdentityProfile,
    VerificationRequest,
    VerifiableCredential,
)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_username(self, value):
        value = value.strip()

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'This username is already registered.'
            )

        return value

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'An account with this email already exists.'
            )

        return value

    def validate_email(self, value):
        value = value.lower().strip()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'An account with this email already exists.'
            )

        domain = value.split('@')[-1]

        try:
            dns.resolver.resolve(domain, 'MX')
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers,
            dns.exception.Timeout,
        ):
            raise serializers.ValidationError(
                'This email domain does not exist or cannot receive email.'
            )

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        IdentityProfile.objects.create(user=user)

        return user


class VerificationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationRequest
        fields = [
            'id',
            'status',
            'verification_method',
            'mock_document_reference',
            'reviewer_note',
            'submitted_at',
            'reviewed_at',
        ]
        read_only_fields = [
            'status',
            'reviewer_note',
            'submitted_at',
            'reviewed_at',
        ]


class VerifiableCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiableCredential
        fields = [
            'credential_id',
            'issuer_did',
            'subject_did',
            'claims',
            'issued_at',
            'expires_at',
            'revoked',
        ]


class IdentityProfileSerializer(serializers.ModelSerializer):
    verification_requests = VerificationRequestSerializer(
        many=True,
        read_only=True
    )
    credentials = VerifiableCredentialSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = IdentityProfile
        fields = [
            'id',
            'is_verified',
            'display_name',
            'country_of_origin',
            'preferred_language',
            'verification_requests',
            'credentials',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['is_verified']