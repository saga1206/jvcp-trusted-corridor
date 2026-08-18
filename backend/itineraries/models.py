from django.db import models
from django.contrib.auth.models import User

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    destination = models.CharField(max_length=200)
    duration_days = models.PositiveSmallIntegerField()
    budget_jpy = models.PositiveIntegerField(null=True, blank=True)
    interests = models.CharField(max_length=300, blank=True)  # comma-separated
    travel_companions = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(max_length=10, default='vi')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.destination} ({self.duration_days}d) — {self.user.username}"


class ItineraryDay(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveSmallIntegerField()
    summary = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['day_number']


class ItineraryItem(models.Model):
    day = models.ForeignKey(ItineraryDay, on_delete=models.CASCADE, related_name='items')
    time_of_day = models.CharField(max_length=50, blank=True)  # "morning", "14:00", etc.
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    estimated_cost_jpy = models.PositiveIntegerField(null=True, blank=True)
    provider = models.ForeignKey('providers.Provider', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['id']