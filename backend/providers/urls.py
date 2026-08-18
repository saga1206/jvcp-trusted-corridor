from django.urls import path
from .views import ProviderListCreateView, ProviderDetailView, ReviewCreateView

urlpatterns = [
    path('', ProviderListCreateView.as_view(), name='provider-list'),
    path('<int:pk>/', ProviderDetailView.as_view(), name='provider-detail'),
    path('<int:provider_id>/reviews/', ReviewCreateView.as_view(), name='provider-review-create'),
]