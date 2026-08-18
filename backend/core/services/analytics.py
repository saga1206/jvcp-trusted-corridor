from core.models import AnalyticsEvent

def track(event_type, user=None, **metadata):
    AnalyticsEvent.objects.create(event_type=event_type, user=user, metadata=metadata)