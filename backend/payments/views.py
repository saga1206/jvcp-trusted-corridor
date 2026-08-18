from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Order, Payment, Refund
from .serializers import OrderSerializer, RefundSerializer, RefundRequestSerializer, PayRequestSerializer
from core.services.analytics import track
from core.services.audit import record
from django.shortcuts import get_object_or_404


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        record('ORDER_CREATED', self.request.user, 'Order', order.id, amount=order.amount_jpy)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PayOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        req = PayRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)

        payment, _ = Payment.objects.get_or_create(order=order)
        payment.method = req.validated_data['method']
        payment.save()

        record('PAYMENT_CREATED', request.user, 'Payment', payment.transaction_id,
               method=payment.method, amount=order.amount_jpy)

        return Response(OrderSerializer(order).data)


class ConfirmPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        payment = order.payment
        payment.status = 'confirmed'
        payment.confirmed_at = timezone.now()
        payment.save()
        order.status = 'paid'
        order.save()

        track('order_paid', user=request.user, amount=order.amount_jpy, method=payment.method)
        record('PAYMENT_COMPLETED', request.user, 'Payment', payment.transaction_id,
               amount=order.amount_jpy)
        record('ORDER_COMPLETED', request.user, 'Order', order.id)

        return Response(OrderSerializer(order).data)


class RequestRefundView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        req = RefundRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        refund = Refund.objects.create(order=order, **req.validated_data)

        track('refund_requested', user=request.user)
        record('REFUND_REQUESTED', request.user, 'Refund', refund.id, amount=refund.amount_jpy)

        return Response(RefundSerializer(refund).data, status=status.HTTP_201_CREATED)