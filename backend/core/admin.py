from django.contrib import admin
from .models import AuditEvent
from .models import ExchangeRate, AnalyticsEvent

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['base_currency', 'target_currency', 'rate', 'source', 'fetched_at']


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'user', 'created_at']
    list_filter = ['event_type']

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_type', 'entity_type', 'entity_id', 'actor', 'timestamp', 'event_hash']
    list_filter = ['event_type', 'entity_type']
    readonly_fields = ['event_hash', 'previous_hash', 'timestamp']

    def has_change_permission(self, request, obj=None):
        return False  # append-only — admin can view, never edit

    def has_delete_permission(self, request, obj=None):
        return False