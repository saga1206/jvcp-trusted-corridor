from django.urls import path
from .views import OrderListCreateView, OrderDetailView, PayOrderView, ConfirmPaymentView, RequestRefundView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/pay/', PayOrderView.as_view(), name='order-pay'),
    path('orders/<int:order_id>/confirm/', ConfirmPaymentView.as_view(), name='order-confirm'),
    path('orders/<int:order_id>/refund/', RequestRefundView.as_view(), name='order-refund'),
]