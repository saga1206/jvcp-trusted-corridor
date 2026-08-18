from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import RemittanceTransfer
from .serializers import RemittanceTransferSerializer, RemittanceQuoteRequestSerializer, RemittanceCreateSerializer
from .services.rate_lookup import quote
from core.services.analytics import track
from core.services.audit import record
from django.shortcuts import get_object_or_404

CURRENCY_MAP = {'jp_to_vn': ('JPY', 'VND'), 'vn_to_jp': ('VND', 'JPY')}

class RemittanceQuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req = RemittanceQuoteRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        send_currency, receive_currency = CURRENCY_MAP[req.validated_data['direction']]
        result = quote(req.validated_data['send_amount'], send_currency, receive_currency)
        return Response({
            "send_amount": req.validated_data['send_amount'],
            "send_currency": send_currency,
            "receive_currency": receive_currency,
            "exchange_rate": result['rate'],
            "service_fee": result['fee'],
            "receive_amount": result['receive_amount'],
            "note": "Simulation only — not connected to real banking infrastructure.",
        })

class RemittanceListCreateView(generics.ListCreateAPIView):
    serializer_class = RemittanceTransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RemittanceTransfer.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        req = RemittanceCreateSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data
        send_currency, receive_currency = CURRENCY_MAP[data['direction']]
        result = quote(data['send_amount'], send_currency, receive_currency)

        transfer = RemittanceTransfer.objects.create(
            sender=request.user,
            recipient_name=data['recipient_name'],
            recipient_account_ref=data['recipient_account_ref'],
            direction=data['direction'],
            send_amount=data['send_amount'],
            send_currency=send_currency,
            exchange_rate=result['rate'],
            service_fee=result['fee'],
            receive_amount=result['receive_amount'],
            receive_currency=receive_currency,
        )
        track('remittance_initiated', user=request.user, amount=str(data['send_amount']), direction=data['direction'])
        record('REMITTANCE_CREATED', request.user, 'RemittanceTransfer', transfer.transaction_id,
               amount=str(data['send_amount']), direction=data['direction'])

        return Response(RemittanceTransferSerializer(transfer).data, status=status.HTTP_201_CREATED)

class RemittanceCompleteView(APIView):
    """Mock 'processing complete' step — a real integration would be webhook-driven."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, transfer_id):
        transfer = get_object_or_404(RemittanceTransfer, id=transfer_id, sender=request.user)
        transfer.status = 'completed'
        transfer.completed_at = timezone.now()
        transfer.save()

        record('REMITTANCE_COMPLETED', request.user, 'RemittanceTransfer', transfer.transaction_id)

        return Response(RemittanceTransferSerializer(transfer).data)