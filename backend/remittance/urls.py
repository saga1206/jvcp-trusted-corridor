from django.urls import path
from .views import RemittanceQuoteView, RemittanceListCreateView, RemittanceCompleteView

urlpatterns = [
    path('quote/', RemittanceQuoteView.as_view(), name='remittance-quote'),
    path('', RemittanceListCreateView.as_view(), name='remittance-list'),
    path('<int:transfer_id>/complete/', RemittanceCompleteView.as_view(), name='remittance-complete'),
]