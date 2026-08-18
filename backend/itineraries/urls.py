from django.urls import path
from .views import ItineraryListView, ItineraryDetailView, GenerateItineraryView

urlpatterns = [
    path('', ItineraryListView.as_view(), name='itinerary-list'),
    path('<int:pk>/', ItineraryDetailView.as_view(), name='itinerary-detail'),
    path('generate/', GenerateItineraryView.as_view(), name='itinerary-generate'),
]