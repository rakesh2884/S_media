from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from s_media_app.models import User

class follow_user(APIView):
    @permission_classes([IsAuthenticated])
    def post(self,request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(user_to_follow)
        return Response({'message': 'You are now following this user'}, status=status.HTTP_200_OK)

class unfollow_user(APIView):
    @permission_classes([IsAuthenticated])
    def post(self,request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'You have unfollowed this user'}, status=status.HTTP_200_OK)
