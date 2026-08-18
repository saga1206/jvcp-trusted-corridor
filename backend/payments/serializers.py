from rest_framework import serializers
from .models import Order, Payment, Refund

class PaymentSerializer(serializers.ModelSerializer):
    qr_payload = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = ['id', 'transaction_id', 'method', 'status', 'qr_payload', 'initiated_at', 'confirmed_at']

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'reason', 'amount_jpy', 'status', 'merchant_note', 'requested_at', 'resolved_at']
        read_only_fields = ['status', 'merchant_note', 'resolved_at']

class OrderSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    refunds = RefundSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'provider', 'description', 'amount_jpy', 'status', 'payment', 'refunds', 'created_at']
        read_only_fields = ['status']

class PayRequestSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['qr_code', 'nfc_tap', 'card_mock'], default='qr_code')

class RefundRequestSerializer(serializers.Serializer):
    reason = serializers.CharField()
    amount_jpy = serializers.IntegerField(min_value=1)