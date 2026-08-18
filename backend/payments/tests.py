from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status

from payments.models import Order, Payment, Refund


@override_settings(RATELIMIT_ENABLE=False)
class PaymentHappyPathTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='payuser', email='payuser@gmail.com', password='x')
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(user=self.user, description='Test booking', amount_jpy=3000)

    def test_full_pay_confirm_refund_flow(self):
        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/pay/', {'method': 'card_mock'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(Payment.objects.filter(order=self.order).exists())

        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/confirm/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')
        self.assertEqual(self.order.payment.status, 'confirmed')

        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/refund/', {
            'reason': 'Change of plans',
            'amount_jpy': 3000,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Refund.objects.filter(order=self.order).exists())

    def test_order_list_only_shows_own_orders(self):
        other_user = User.objects.create_user(username='otherpayuser', email='other@gmail.com', password='x')
        Order.objects.create(user=other_user, description='Not yours', amount_jpy=1000)

        resp = self.client.get('/api/v1/payments/orders/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        ids = [o['id'] for o in resp.data]
        self.assertIn(self.order.id, ids)
        self.assertEqual(len(ids), 1)


@override_settings(RATELIMIT_ENABLE=False)
class PaymentIDORTests(APITestCase):
    """Regression coverage for the IDOR gap found and fixed on 2026-08-18:
    Order lookups by ID must never leak or act on another user's order."""

    def setUp(self):
        self.owner = User.objects.create_user(username='idorowner', email='idorowner@gmail.com', password='x')
        self.attacker = User.objects.create_user(username='idorattacker', email='idorattacker@gmail.com', password='x')
        self.order = Order.objects.create(user=self.owner, description='Owner order', amount_jpy=5000)
        self.client.force_authenticate(user=self.attacker)

    def test_attacker_cannot_view_order(self):
        resp = self.client.get(f'/api/v1/payments/orders/{self.order.id}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_attacker_cannot_pay_order(self):
        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/pay/', {'method': 'card_mock'})
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_attacker_cannot_confirm_order(self):
        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/confirm/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_attacker_cannot_refund_order(self):
        resp = self.client.post(f'/api/v1/payments/orders/{self.order.id}/refund/', {
            'reason': 'not mine',
            'amount_jpy': 5000,
        })
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
