from django.contrib import admin
from django.utils import timezone
from .models import IdentityProfile, VerificationRequest, VerifiableCredential
from core.services.audit import record

@admin.register(IdentityProfile)
class IdentityProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified', 'preferred_language', 'created_at']
    list_filter = ['is_verified', 'preferred_language']

@admin.action(description="Approve selected requests and issue a mock Verifiable Credential")
def approve_and_issue_vc(modeladmin, request, queryset):
    for vr in queryset:
        vr.status = 'approved'
        vr.reviewed_at = timezone.now()
        vr.save()
        vr.profile.is_verified = True
        vr.profile.save()

        record('IDENTITY_APPROVED', request.user, 'VerificationRequest', vr.id,
               verification_method=vr.verification_method)

        did = f"did:mock:user:{vr.profile.user.id}"
        record('DID_CREATED', request.user, 'IdentityProfile', vr.profile.id, did=did)

        vc = VerifiableCredential.objects.create(
            profile=vr.profile,
            subject_did=did,
            claims={
                "verified_country": vr.profile.country_of_origin or "unknown",
                "verification_method": vr.verification_method,
                "platform": "jvcp",
            },
        )
        record('VC_ISSUED', request.user, 'VerifiableCredential', vc.credential_id,
               subject_did=did)

@admin.action(description="Reject selected requests")
def reject_requests(modeladmin, request, queryset):
    for vr in queryset:
        vr.status = 'rejected'
        vr.reviewed_at = timezone.now()
        vr.save()
        record('IDENTITY_REJECTED', request.user, 'VerificationRequest', vr.id)

@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'status', 'verification_method', 'submitted_at']
    list_filter = ['status', 'verification_method']
    actions = [approve_and_issue_vc, reject_requests]

@admin.register(VerifiableCredential)
class VerifiableCredentialAdmin(admin.ModelAdmin):
    list_display = ['credential_id', 'profile', 'issuer_did', 'issued_at', 'revoked']