from rest_framework import serializers
from .models import RemittanceTransfer

class RemittanceQuoteRequestSerializer(serializers.Serializer):
    direction = serializers.ChoiceField(choices=['jp_to_vn', 'vn_to_jp'])
    send_amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=1)

class RemittanceTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemittanceTransfer
        fields = ['id', 'transaction_id', 'recipient_name', 'recipient_account_ref', 'direction',
                  'send_amount', 'send_currency', 'exchange_rate', 'service_fee',
                  'receive_amount', 'receive_currency', 'status', 'created_at', 'completed_at']
        read_only_fields = ['transaction_id', 'exchange_rate', 'service_fee', 'receive_amount',
                             'status', 'created_at', 'completed_at']

class RemittanceCreateSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(max_length=150)
    recipient_account_ref = serializers.CharField(max_length=100)
    direction = serializers.ChoiceField(choices=['jp_to_vn', 'vn_to_jp'])
    send_amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=1)