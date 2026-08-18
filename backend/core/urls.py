from django.urls import path
from .views import LatestRatesView, AuditChainVerifyView

urlpatterns = [
    path('rates/', LatestRatesView.as_view(), name='rates-latest'),
    path('audit/verify/', AuditChainVerifyView.as_view(), name='audit-verify'),
]