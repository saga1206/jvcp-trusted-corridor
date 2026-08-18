"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from identity.views import ThrottledTokenObtainPairView

from core.dashboard import AdminDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/token/', ThrottledTokenObtainPairView.as_view()),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/v1/identity/', include('identity.urls')),
    path('api/v1/providers/', include('providers.urls')),
    path('api/v1/itineraries/', include('itineraries.urls')),
    path('api/v1/assistant/', include('assistant.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/', include('core.urls')),
    path('api/v1/marketplace/', include('marketplace.urls')),
    path('api/v1/admin/dashboard/', AdminDashboardView.as_view()),
    path('api/v1/remittance/', include('remittance.urls')),
]
