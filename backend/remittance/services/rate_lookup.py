from core.models import ExchangeRate
from decimal import Decimal

FEE_RATE = Decimal('0.015')  # 1.5% mock service fee — documented as illustrative, not a real pricing decision

def get_rate(base_currency, target_currency):
    rate_obj = ExchangeRate.objects.filter(
        base_currency=base_currency, target_currency=target_currency
    ).order_by('-fetched_at').first()
    if not rate_obj:
        raise ValueError(f"No mock rate configured for {base_currency}->{target_currency}. Add one via /admin/.")
    return rate_obj.rate

def quote(send_amount, send_currency, receive_currency):
    rate = get_rate(send_currency, receive_currency)
    fee = (Decimal(send_amount) * FEE_RATE).quantize(Decimal('0.01'))
    net_send = Decimal(send_amount) - fee
    receive_amount = (net_send * rate).quantize(Decimal('0.01'))
    return {
        "rate": rate,
        "fee": fee,
        "receive_amount": receive_amount,
    }