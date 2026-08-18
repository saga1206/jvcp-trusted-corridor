from django.contrib import admin
from .models import Order, Payment, Refund

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'amount_jpy', 'status', 'created_at']
    list_filter = ['status']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'status', 'confirmed_at']

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount_jpy', 'status', 'requested_at']
    list_filter = ['status']