from django.db import models
import hashlib
import json

class ExchangeRate(models.Model):
    base_currency = models.CharField(max_length=3)     # e.g. JPY
    target_currency = models.CharField(max_length=3)    # e.g. VND
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    source = models.CharField(max_length=100, default='mock/demo')
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fetched_at']


class AnalyticsEvent(models.Model):
    EVENT_TYPES = [
        ('user_registered', 'User Registered'),
        ('itinerary_created', 'Itinerary Created'),
        ('assistant_message', 'Assistant Message'),
        ('search', 'Search'),
        ('order_created', 'Order Created'),
        ('order_paid', 'Order Paid'),
        ('refund_requested', 'Refund Requested'),
        ('review_posted', 'Review Posted'),
    ]
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AuditEvent(models.Model):
    EVENT_TYPES = [
        ('IDENTITY_SUBMITTED', 'Identity Submitted'),
        ('IDENTITY_APPROVED', 'Identity Approved'),
        ('IDENTITY_REJECTED', 'Identity Rejected'),
        ('DID_CREATED', 'DID Created'),
        ('VC_ISSUED', 'VC Issued'),
        ('VC_REVOKED', 'VC Revoked'),
        ('PAYMENT_CREATED', 'Payment Created'),
        ('PAYMENT_COMPLETED', 'Payment Completed'),
        ('PAYMENT_FAILED', 'Payment Failed'),
        ('ORDER_CREATED', 'Order Created'),
        ('ORDER_COMPLETED', 'Order Completed'),
        ('REFUND_REQUESTED', 'Refund Requested'),
        ('REMITTANCE_CREATED', 'Remittance Created'),
        ('REMITTANCE_COMPLETED', 'Remittance Completed'),
    ]
    actor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=40, choices=EVENT_TYPES)
    entity_type = models.CharField(max_length=50)
    entity_id = models.CharField(max_length=50)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=64, blank=True)
    event_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.pk:
            last = AuditEvent.objects.order_by('-id').first()
            self.previous_hash = last.event_hash if last else '0' * 64
            payload = json.dumps({
                "actor": self.actor_id,
                "event_type": self.event_type,
                "entity_type": self.entity_type,
                "entity_id": self.entity_id,
                "metadata": self.metadata,
                "previous_hash": self.previous_hash,
            }, sort_keys=True, default=str)
            self.event_hash = hashlib.sha256(payload.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_type} — {self.entity_type}#{self.entity_id}"