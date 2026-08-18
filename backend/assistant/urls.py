from django.urls import path
from .views import ThreadListView, SendMessageView

urlpatterns = [
    path('threads/', ThreadListView.as_view(), name='thread-list'),
    path('message/', SendMessageView.as_view(), name='assistant-message'),
]