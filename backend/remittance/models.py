from django.db import models
from django.contrib.auth.models import User
import uuid

class RemittanceTransfer(models.Model):
    DIRECTION_CHOICES = [
        ('jp_to_vn', 'Japan → Vietnam'),
        ('vn_to_jp', 'Vietnam → Japan'),
    ]
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    recipient_name = models.CharField(max_length=150)
    recipient_account_ref = models.CharField(max_length=100, help_text="Mock account reference — never a real bank number")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    send_amount = models.DecimalField(max_digits=14, decimal_places=2)
    send_currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    receive_amount = models.DecimalField(max_digits=14, decimal_places=2)
    receive_currency = models.CharField(max_length=3)
    transaction_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_id} ({self.status})"