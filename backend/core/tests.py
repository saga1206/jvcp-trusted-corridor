from django.contrib.auth.models import User
from django.test import TestCase

from core.models import AuditEvent
from core.services.audit import record, verify_chain


class AuditChainTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='audituser', email='audituser@gmail.com', password='x')

    def test_chain_valid_after_multiple_events(self):
        record('ORDER_CREATED', self.user, 'Order', 1, amount=1000)
        record('PAYMENT_CREATED', self.user, 'Payment', 'txn-abc', method='card_mock')
        record('PAYMENT_COMPLETED', self.user, 'Payment', 'txn-abc', amount=1000)

        result = verify_chain()
        self.assertTrue(result['valid'])
        self.assertEqual(result['events_checked'], 3)

    def test_events_link_via_previous_hash(self):
        e1 = record('ORDER_CREATED', self.user, 'Order', 2)
        e2 = record('ORDER_COMPLETED', self.user, 'Order', 2)
        self.assertEqual(e2.previous_hash, e1.event_hash)

    def test_tampering_detected(self):
        record('ORDER_CREATED', self.user, 'Order', 3, amount=500)
        e2 = record('PAYMENT_CREATED', self.user, 'Payment', 'txn-tamper', amount=500)
        record('PAYMENT_COMPLETED', self.user, 'Payment', 'txn-tamper', amount=500)

        # Tamper with a middle event's metadata without recomputing its hash —
        # simulates an attacker editing the DB directly.
        AuditEvent.objects.filter(pk=e2.pk).update(metadata={'amount': 999999})

        result = verify_chain()
        self.assertFalse(result['valid'])
        self.assertEqual(result['broken_at_event_id'], e2.id)

    def test_empty_chain_is_valid(self):
        result = verify_chain()
        self.assertTrue(result['valid'])
        self.assertEqual(result['events_checked'], 0)
