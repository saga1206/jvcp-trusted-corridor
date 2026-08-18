from django.urls import path
from .views import (
    RegisterView,
    GoogleLoginView,
    MyProfileView,
    SubmitVerificationView,
    EmailVerificationView,
    VerifyCredentialView,
    RevokeCredentialView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MyProfileView.as_view(), name='identity-me'),
    path('verify/', SubmitVerificationView.as_view(), name='identity-verify'),
    path('google/', GoogleLoginView.as_view(), name='google-login'),
    path('verify-email/<uuid:token>/', EmailVerificationView.as_view(), name='verify-email'),
    path('credentials/<str:credential_id>/verify/', VerifyCredentialView.as_view(), name='credential-verify'),
    path('credentials/<str:credential_id>/revoke/', RevokeCredentialView.as_view(), name='credential-revoke'),
]