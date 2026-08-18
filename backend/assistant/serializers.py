from rest_framework import serializers
from .models import ConversationThread, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'created_at']

class ConversationThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ConversationThread
        fields = ['id', 'messages', 'created_at']

class SendMessageSerializer(serializers.Serializer):
    thread_id = serializers.IntegerField(required=False, allow_null=True)
    message = serializers.CharField()