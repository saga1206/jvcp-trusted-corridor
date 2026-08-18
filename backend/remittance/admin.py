from django.contrib import admin
from .models import RemittanceTransfer

@admin.register(RemittanceTransfer)
class RemittanceTransferAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'sender', 'direction', 'send_amount', 'receive_amount', 'status', 'created_at']
    list_filter = ['direction', 'status']