from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .services.audit import verify_chain


class LatestRatesView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        pairs = ExchangeRate.objects.values_list('base_currency', 'target_currency').distinct()
        latest_ids = [
            ExchangeRate.objects.filter(base_currency=b, target_currency=t).first().id
            for b, t in pairs
        ]
        return ExchangeRate.objects.filter(id__in=latest_ids)


class AuditChainVerifyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(verify_chain())