from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import ConversationThread, Message
from .serializers import ConversationThreadSerializer, SendMessageSerializer
from .services.ai_assistant import get_reply
from core.services.analytics import track


class ThreadListView(generics.ListAPIView):
    serializer_class = ConversationThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ConversationThread.objects.filter(user=self.request.user)


@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='post')
class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        req = SendMessageSerializer(data=request.data)
        req.is_valid(raise_exception=True)
        data = req.validated_data

        if data.get('thread_id'):
            thread = ConversationThread.objects.get(id=data['thread_id'], user=request.user)
        else:
            thread = ConversationThread.objects.create(user=request.user)

        Message.objects.create(thread=thread, role='user', content=data['message'])

        history = list(thread.messages.all())
        reply_text = get_reply(request.user, history[:-1], data['message'])

        assistant_msg = Message.objects.create(thread=thread, role='assistant', content=reply_text)

        track('assistant_message', user=request.user)

        return Response({
            'thread_id': thread.id,
            'reply': assistant_msg.content,
        }, status=status.HTTP_201_CREATED)