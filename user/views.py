import time

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail

from jwt import encode, decode
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from s_media.settings import EMAIL_HOST_USER, SECRET_KEY, SECRET_KEY2, \
    RESET_LINK
from utils.error_handler import error_response
from utils.success_handler import \
    success_response

from user.utils import check_forgot_field, confirm_password_check
from user.models import User, Link
from user.serializers import UserSerializer, LinkSerializer


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


class forgot_password(APIView):
    serializer_class = LinkSerializer

    def post(self, request):
        serializer = LinkSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.data['user']
            try:
                users = User.objects.get(id=user)
            except User.DoesNotExist:
                return error_response('User not found', 404)
            now = int(time.time())
            token = encode({"username": users.username,
                           "action": "reset_link",
                            "timestamp": now}, SECRET_KEY)
            print(token)
            encoded_token = encode({"token": token}, SECRET_KEY2)
            try:
                user_exist = Link.objects.get(user=user)
                user_exist.delete()
            finally:
                now = int(time.time())
                expired_time = now + 60
                token = token
                serializer.save(token=encoded_token,
                                isUsed=False,
                                expired_time=expired_time)
                reset_link = RESET_LINK+token
                subject = 'Reset Your Password'
                message = "Hey ," + users.username + \
                    " To reset your password. Your link is : " + \
                    reset_link
                email_from = EMAIL_HOST_USER
                recipient_list = [users.email, ]
                send_mail(subject,
                          message,
                          email_from,
                          recipient_list)
                return success_response('OTP sent successfully', 200)
        return error_response(serializer.errors, 400)


class reset_password(APIView):
    def post(self, request, token):
        decoded_link = decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded_link.get('username')
        if check_forgot_field:
            new_password = request.POST.get('new_password')
            if confirm_password_check:
                try:
                    users = User.objects.get(username=username)
                except User.DoesNotExist:
                    return error_response('user not exist', 404)
                try:
                    user_exist = Link.objects.get(user=users.id)
                except Link.DoesNotExist:
                    return error_response('no link generate', 400)
                expired_time = user_exist.expired_time
                encoded_token = encode({"token": token}, SECRET_KEY2)
                now = int(time.time())
                if now < expired_time and user_exist.isUsed is False:
                    if user_exist.token == encoded_token:
                        user_exist.isUsed = True
                        user_exist.save()
                        users.password = make_password(new_password)
                        users.save()
                        return success_response("password reset \
                                                 successfully",
                                                200)
                    else:
                        return error_response('Link expired', 400)
                else:
                    return error_response("Link expired", 400)
            else:
                return error_response('password not match', 400)
        else:
            return error_response('fields are missing', 400)


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
