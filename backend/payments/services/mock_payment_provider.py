import uuid
from django.utils import timezone

class PaymentProvider:
    """Mock implementation. A real provider (Stripe, Komoju) would implement the same interface."""

    def initiate(self, order):
        from .models import Payment  # local import avoids circulars if needed
        return {"transaction_id": str(uuid.uuid4()), "status": "initiated"}

    def confirm(self, payment):
        payment.status = "confirmed"
        payment.confirmed_at = timezone.now()
        payment.save()
        return payment