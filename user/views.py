import time

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail

from jwt import encode,decode
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from s_media.settings import EMAIL_HOST_USER,SECRET_KEY
from utils.error_handler import error_response
from utils.success_handler import \
    success_response

from user.models import User
from user.serializers import UserSerializer



class register(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(password=make_password(request.data['password']))
            return success_response(serializer.data, 200)
        return error_response(serializer.errors, 400)


class login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return success_response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, 200)
        return error_response('Invalid credentials', 401)


class get_profile(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        print(type(user.role))
        serializer = UserSerializer(user)
        return success_response(serializer.data, 200)


class change_password(APIView):
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_password = request.data['updated_password']
            if check_password(updated_password, user.password):
                return error_response("new password cannot be same", 400)
            else:
                serializer.save(password=make_password(updated_password))
                return success_response("password change successfully", 200)
        return error_response(serializer.errors, 400)


class update_profile(APIView):
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, 200)
        return error_response(serializer.errors, 400)


class delete_self_account(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user
        user.delete()
        return success_response('Your account deleted successfully', 200)


class view_others_profile(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, user_id):
        try:
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return error_response('User not found', 404)

        serializer = UserSerializer(user_profile)
        return success_response(serializer.data, 302)
