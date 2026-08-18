from django.db import models
from django.contrib.auth.models import User
import uuid

class IdentityProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='identity_profile')
    is_verified = models.BooleanField(default=False)
    display_name = models.CharField(max_length=150, blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('vi', 'Vietnamese'), ('ja', 'Japanese'), ('en', 'English')],
        default='vi',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({'verified' if self.is_verified else 'unverified'})"

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='email_verification'
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email verification for {self.user.username}"
    

class VerificationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    METHOD_CHOICES = [
        ('ekyc_document', 'eKYC — Document scan'),
        ('ekyc_selfie', 'eKYC — Selfie liveness check'),
        ('did_vc_import', 'Import existing DID/Verifiable Credential'),
    ]
    profile = models.ForeignKey(IdentityProfile, on_delete=models.CASCADE, related_name='verification_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verification_method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='ekyc_document')
    mock_document_reference = models.CharField(max_length=100, blank=True)  # never a real doc — simulation only
    reviewer_note = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"VerificationRequest #{self.pk} ({self.status})"


class VerifiableCredential(models.Model):
    """Mock W3C-style Verifiable Credential issued on approval. Not a real DID/VC implementation —
    models the shape (issuer/subject/claims/proof) so the architecture is swappable for a real
    DID/VC or eKYC vendor later."""
    profile = models.ForeignKey(IdentityProfile, on_delete=models.CASCADE, related_name='credentials')
    credential_id = models.CharField(max_length=64, default=uuid.uuid4, unique=True, editable=False)
    issuer_did = models.CharField(max_length=100, default='did:mock:jvcp-platform')
    subject_did = models.CharField(max_length=100, blank=True)  # mock DID assigned to the user
    claims = models.JSONField(default=dict)  # e.g. {"verified_country": "VN", "age_over_18": true}
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    def __str__(self):
        return f"VC {self.credential_id} — {self.profile.user.username}"