from rest_framework import serializers
from .models import Itinerary, ItineraryDay, ItineraryItem

class ItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = ['id', 'time_of_day', 'title', 'description', 'estimated_cost_jpy', 'provider']

class ItineraryDaySerializer(serializers.ModelSerializer):
    items = ItineraryItemSerializer(many=True, read_only=True)

    class Meta:
        model = ItineraryDay
        fields = ['id', 'day_number', 'summary', 'items']

class ItinerarySerializer(serializers.ModelSerializer):
    days = ItineraryDaySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'destination', 'duration_days', 'budget_jpy', 'interests',
                  'travel_companions', 'preferred_language', 'days', 'created_at']

class ItineraryRequestSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length=200)
    duration_days = serializers.IntegerField(min_value=1, max_value=30)
    budget_jpy = serializers.IntegerField(required=False, allow_null=True, default=None)
    interests = serializers.CharField(required=False, allow_blank=True)
    travel_companions = serializers.CharField(required=False, allow_blank=True, default='')
    preferred_language = serializers.ChoiceField(choices=['vi', 'ja', 'en'], default='vi')