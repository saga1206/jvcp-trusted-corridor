from django.contrib import admin
from .models import ConversationThread, Message

admin.site.register(ConversationThread)
admin.site.register(Message)