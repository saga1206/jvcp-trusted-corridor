from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Itinerary, ItineraryDay, ItineraryItem
from .serializers import ItinerarySerializer, ItineraryRequestSerializer
from .services.ai_planner import generate_itinerary
from core.services.analytics import track


class ItineraryListView(generics.ListAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


class ItineraryDetailView(generics.RetrieveAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user=self.request.user)


@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='post')
class GenerateItineraryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req = ItineraryRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data

        ai_result = generate_itinerary(**data)

        with transaction.atomic():
            itinerary = Itinerary.objects.create(user=request.user, **data)
            for day_data in ai_result['days']:
                day = ItineraryDay.objects.create(
                    itinerary=itinerary,
                    day_number=day_data['day_number'],
                    summary=day_data.get('summary', ''),
                )
                for item_data in day_data.get('items', []):
                    ItineraryItem.objects.create(
                        day=day,
                        time_of_day=item_data.get('time_of_day', ''),
                        title=item_data['title'],
                        description=item_data.get('description', ''),
                        estimated_cost_jpy=item_data.get('estimated_cost_jpy'),
                    )

        track('itinerary_created', user=request.user, destination=data['destination'])

        return Response(ItinerarySerializer(itinerary).data, status=status.HTTP_201_CREATED)