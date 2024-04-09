from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from s_media_app.handlers.error_handler import error_response
from s_media_app.handlers.success_handler import success_response
from s_media_app.models import User

class follow_user(APIView):
    @permission_classes([IsAuthenticated])
    def post(self,request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return error_response('User not found', 404)

        request.user.following.add(user_to_follow)
        return success_response('You are now following this user', 200)

class unfollow_user(APIView):
    @permission_classes([IsAuthenticated])
    def post(self,request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return error_response('User not found', 404)

        request.user.following.remove(user_to_unfollow)
        return success_response('You have unfollowed this user', 200)