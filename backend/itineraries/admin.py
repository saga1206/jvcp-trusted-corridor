from django.contrib import admin
from .models import Itinerary, ItineraryDay, ItineraryItem

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ['destination', 'user', 'duration_days', 'created_at']

admin.site.register(ItineraryDay)
admin.site.register(ItineraryItem)