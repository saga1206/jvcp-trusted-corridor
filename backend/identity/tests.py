from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from identity.models import IdentityProfile, EmailVerificationToken, VerificationRequest, VerifiableCredential


@override_settings(RATELIMIT_ENABLE=False)
class RegistrationTests(APITestCase):
    def test_register_success(self):
        resp = self.client.post('/api/v1/identity/register/', {
            'username': 'newuser1',
            'email': 'newuser1@gmail.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='newuser1')
        self.assertFalse(user.is_active)
        self.assertTrue(EmailVerificationToken.objects.filter(user=user).exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username='dupeuser', email='dupe1@gmail.com', password='x')
        resp = self.client.post('/api/v1/identity/register/', {
            'username': 'dupeuser',
            'email': 'dupe2@gmail.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email(self):
        User.objects.create_user(username='someoneelse', email='taken@gmail.com', password='x')
        resp = self.client.post('/api/v1/identity/register/', {
            'username': 'freshusername',
            'email': 'taken@gmail.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_password_mismatch(self):
        resp = self.client.post('/api/v1/identity/register/', {
            'username': 'mismatchuser',
            'email': 'mismatch@gmail.com',
            'password': 'StrongPass123!',
            'confirm_password': 'DifferentPass456!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', resp.data)


@override_settings(RATELIMIT_ENABLE=False)
class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='unverified', email='unverified@gmail.com', password='x')
        self.user.is_active = False
        self.user.save()
        self.token = EmailVerificationToken.objects.create(user=self.user)

    def test_valid_token_activates_user(self):
        resp = self.client.get(f'/api/v1/identity/verify-email/{self.token.token}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertIn('access', resp.data)

    def test_invalid_token_rejected(self):
        resp = self.client.get('/api/v1/identity/verify-email/00000000-0000-0000-0000-000000000000/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class LoginRateLimitTests(APITestCase):
    def test_sixth_login_attempt_blocked(self):
        User.objects.create_user(username='ratelimituser', email='rl@gmail.com', password='CorrectPass123!')
        for i in range(5):
            resp = self.client.post('/api/v1/auth/token/', {
                'username': 'ratelimituser',
                'password': 'wrongpassword',
            })
            self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        resp = self.client.post('/api/v1/auth/token/', {
            'username': 'ratelimituser',
            'password': 'wrongpassword',
        })
        self.assertEqual(resp.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


@override_settings(RATELIMIT_ENABLE=False)
class CredentialLifecycleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vcuser', email='vcuser@gmail.com', password='x')
        self.profile = IdentityProfile.objects.create(user=self.user)
        self.admin = User.objects.create_superuser(username='vcadmin', email='vcadmin@gmail.com', password='x')

    def test_issued_credential_verifiable_and_revocable(self):
        vc = VerifiableCredential.objects.create(
            profile=self.profile,
            subject_did='did:mock:subject123',
            claims={'age_over_18': True},
        )

        resp = self.client.get(f'/api/v1/identity/credentials/{vc.credential_id}/verify/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['valid'])
        self.assertFalse(resp.data['revoked'])

        self.client.force_authenticate(user=self.admin)
        resp = self.client.post(f'/api/v1/identity/credentials/{vc.credential_id}/revoke/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=None)
        resp = self.client.get(f'/api/v1/identity/credentials/{vc.credential_id}/verify/')
        self.assertTrue(resp.data['revoked'])
        self.assertFalse(resp.data['valid'])

    def test_non_admin_cannot_revoke(self):
        vc = VerifiableCredential.objects.create(profile=self.profile, subject_did='did:mock:subject456')
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(f'/api/v1/identity/credentials/{vc.credential_id}/revoke/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
