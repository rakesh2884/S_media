from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from utils.error_handler import error_response
from utils.success_handler import \
    success_response
from message.models import Message, Notification
from message.serializers import MessageSerializer


class send_message(APIView):
    serializer_class = MessageSerializer

    @permission_classes([IsAuthenticated])
    def post(self, request, user_id):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=request.user.id, receiver_id=user_id)
            notifi = "you received an dm from ", request.user.username
            n = Notification(user_id=user_id,
                             sender_id=request.user.id,
                             subject=notifi)
            n.save()
            return success_response(serializer.data, 200)
        return error_response(serializer.errors, 400)


class view_message(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, sender_id):
        user_message = Message.objects.filter(sender_id=sender_id,
                                              receiver_id=request.user)
        serializer = MessageSerializer(user_message, many=True)
        return success_response(serializer.data, 302)


class delete_message(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request, sender_id):
        try:
            message = Message.objects.get(sender_id=sender_id,
                                          receiver_id=request.user)
        except Message.DoesNotExist:
            return error_response('Message not found', 404)

        message.delete()
        return success_response('Message deleted successfully', 200)


class view_notifications(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user). \
            order_by('created_at')
        for notification in notifications:
            notification_data = {'user': notification.user.id,
                                 'sender': notification.sender.id,
                                 'subject': notification.subject}
        return success_response(notification_data, status=200)
