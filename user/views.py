import random
import re

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

import base64
from jwt import encode, decode
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from s_media.settings import SECRET_KEY, SECRET_KEY2, \
    RESET_LINK, ACTIVATE_LINK, CURRENT_TIME
from utils.error_handler import error_response
from utils.success_handler import \
    success_response

from user.utils import check_forgot_field, confirm_password_check, send_email
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
        try:
            user_check = User.objects.get(username=username)
        except User.DoesNotExist:
            return error_response('User not exist', 404)
        while user_check.login_attempt <= 3 and user_check.is_active is True:
            user = authenticate(username=username, password=password)
            if user:
                user_check.login_attempt = 1
                user_check.save()
                refresh = RefreshToken.for_user(user)
                return success_response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }, 200)
            user_check.login_attempt += 1
            user_check.save()
            return error_response('Wrong password, Try again', 401)
        user_check.is_active = False
        user_check.save()
        prefix = str(random.randint(500, 5000))
        suffix = str(random.randint(500, 5000))
        username = str(username)
        encoded_prefix = base64.b64encode(prefix.encode()).decode()
        encoded_suffix = base64.b64encode(suffix.encode()).decode()
        encoded_username = base64.b64encode(username.encode()).decode()
        links = encoded_prefix + encoded_username + encoded_suffix
        try:
            link = Link.objects.get(user=user_check.id)
            link.delete()
        finally:
            expired_time = CURRENT_TIME + 60
            link = Link(token=links, isUsed=False, expired_time=expired_time,
                        user_id=user_check.id)
            link.save()
            activation_link = f"{ACTIVATE_LINK}?links={links}"
            subject = 'Unauthorized access'
            message = "Hey ," + user_check.username + \
                      " someone unauthorized try to access your account, so" \
                      "your account is deactivated.If you are making the" \
                      " attempt then deactivate your account by this link: " \
                      + activation_link
            send_email(subject, message, user_check.email)
            return success_response('Deactivation Link sent successfully', 200)


class activate(APIView):
    def get(self, request):
        links = request.GET.get('links')
        decoded_link = base64.b64decode(links).decode()
        username = re.sub(r'[~^0-9]', '', decoded_link)
        try:
            users = User.objects.get(username=str(username))
        except User.DoesNotExist:
            return error_response('user not exist', 404)
        try:
            user_exist = Link.objects.get(user=users.id)
        except Link.DoesNotExist:
            return error_response('no link generate', 400)
        expired_time = user_exist.expired_time
        if CURRENT_TIME < expired_time and user_exist.isUsed is False:
            if user_exist.token == links:
                user_exist.isUsed = True
                user_exist.save()
                users.is_active = True
                users.login_attempt = 1
                users.save()
                return success_response("Account activated successfully", 200)
            else:
                return error_response('Link expired', 400)
        else:
            return error_response("Link expired", 400)


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
            prefix = str(random.randint(500, 5000))
            suffix = str(random.randint(500, 5000))
            username = str(users.username)
            encoded_prefix = base64.b64encode(prefix.encode()).decode()
            encoded_suffix = base64.b64encode(suffix.encode()).decode()
            encoded_username = base64.b64encode(username.encode()).decode()
            token = encoded_prefix + encoded_username + encoded_suffix
            encoded_token = encode({"token": token}, SECRET_KEY2)
            try:
                user_exist = Link.objects.get(user=user)
                user_exist.delete()
            finally:
                expired_time = CURRENT_TIME + 60
                token = token
                serializer.save(token=encoded_token,
                                isUsed=False,
                                expired_time=expired_time)
                reset_link = RESET_LINK+token
                subject = 'Reset Your Password'
                message = "Hey ," + users.username + \
                    " To reset your password. Your link is : " + \
                    reset_link
                send_email(subject, message, users.email)
                return success_response('OTP sent successfully', 200)
        return error_response(serializer.errors, 400)


class reset_password(APIView):
    def post(self, request, token):
        decoded_link = base64.b64decode(token).decode()
        username = re.sub(r'[~^0-9]', '', decoded_link)
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
                if CURRENT_TIME < expired_time and user_exist.isUsed is False:
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
