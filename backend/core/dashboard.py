from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from identity.models import IdentityProfile, VerificationRequest
from providers.models import Provider, Review
from payments.models import Order, Refund
from itineraries.models import Itinerary
from assistant.models import Message
from core.models import AnalyticsEvent

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        refunded = Refund.objects.filter(status='completed').count()
        return Response({
            "acquisition": {
                "total_users": User.objects.count(),
                "verified_users": IdentityProfile.objects.filter(is_verified=True).count(),
            },
            "engagement": {
                "itineraries_created": Itinerary.objects.count(),
                "assistant_messages": Message.objects.filter(role='user').count(),
                "searches": AnalyticsEvent.objects.filter(event_type='search').count(),
            },
            "trust": {
                "pending_verifications": VerificationRequest.objects.filter(status='pending').count(),
                "providers_verified": Provider.objects.filter(is_verified=True).count(),
                "providers_total": Provider.objects.count(),
                "avg_provider_rating": Review.objects.aggregate(avg=Avg('rating'))['avg'],
            },
            "commerce": {
                "orders_total": total_orders,
                "orders_paid": Order.objects.filter(status='paid').count(),
                "refund_rate": round(refunded / total_orders, 3) if total_orders else 0,
            },
        })