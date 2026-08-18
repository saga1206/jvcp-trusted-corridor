from django.db import models
from django.contrib.auth.models import User
from providers.models import Provider
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, related_name='orders')
    description = models.CharField(max_length=300)
    amount_jpy = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]
    METHOD_CHOICES = [
        ('qr_code', 'QR code (scan to pay)'),
        ('nfc_tap', 'NFC tap'),
        ('card_mock', 'Card (mock)'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='qr_code')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    initiated_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    @property
    def qr_payload(self):
        # Mock payload — a real integration would encode a signed payment request per provider spec
        return f"jvcp-pay://{self.transaction_id}?amount={self.order.amount_jpy}&currency=JPY"


class Refund(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    reason = models.TextField()
    amount_jpy = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    merchant_note = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)