from django.urls import path
from .views import MarketplaceSearchView

urlpatterns = [
    path('search/', MarketplaceSearchView.as_view(), name='marketplace-search'),
]