from rest_framework import generics, permissions
from django.db.models import Q
from providers.models import Provider
from providers.serializers import ProviderSerializer
from core.services.analytics import track


class MarketplaceSearchView(generics.ListAPIView):
    serializer_class = ProviderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Provider.objects.filter(is_verified=True)
        q = self.request.query_params.get('q')
        category = self.request.query_params.get('category')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
            track('search', user=self.request.user if self.request.user.is_authenticated else None, query=q)
        if category:
            qs = qs.filter(category=category)
        return qs