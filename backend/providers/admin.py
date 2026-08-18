from django.contrib import admin
from .models import Provider, ProviderVerification, Review

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_verified', 'location']
    list_filter = ['category', 'is_verified']

@admin.register(ProviderVerification)
class ProviderVerificationAdmin(admin.ModelAdmin):
    list_display = ['provider', 'status', 'submitted_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['provider', 'author', 'rating', 'created_at']