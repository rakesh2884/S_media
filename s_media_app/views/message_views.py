from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from s_media_app.models import User,Message,Notification
from s_media_app.serializers import MessageSerializer

class send_message(APIView):
    serializer_class = MessageSerializer
    @permission_classes([IsAuthenticated])
    def post(self,request,user_id):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender_id=request.user.id,receiver_id=user_id)
            user=User.objects.get(id=request.user.id)
            notifi="you received an dm from ",request.user.username
            n=Notification(user_id=user_id,sender_id=request.user.id,subject=notifi)
            n.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class view_message(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request,sender_id):
        user_message = Message.objects.filter(sender_id=sender_id,receiver_id=request.user)
        serializer = MessageSerializer(user_message, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)

class delete_message(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self,request,sender_id):
        try:
            message = Message.objects.get(sender_id=sender_id, receiver_id=request.user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        Message.delete()
        return Response({'message': 'Message deleted successfully'}, status=status.HTTP_400_BAD_REQUEST)
    
class view_notifications(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('created_at')
        for notification in notifications:
            notification_data = {'user': notification.user.id, 'sender': notification.sender.id, 'subject': notification.subject} 
        return Response(notification_data,status=status.HTTP_202_ACCEPTED)
