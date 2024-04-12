import time

from django_otp.oath import TOTP
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from s_media.settings import EMAIL_HOST_USER
from utils.error_handler import error_response
from utils.success_handler import \
    success_response

from user.utils import check_forgot_field, confirm_password_check
from user.models import User, OTP
from user.serializers import UserSerializer, OTPSerializer


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
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = OTPSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            value = b'12345678901234567890'
            user = request.data['user']
            try:
                users = User.objects.get(id=user)
            except User.DoesNotExist:
                return error_response('User not found', 404)
            totp = TOTP(key=value,
                        step=30,
                        digits=6)
            try:
                user_exist = OTP.objects.get(user=user)
                user_exist.delete()
            finally:
                now = int(time.time())
                expired_time = now + 60
                token = totp.token()
                serializer.save(otp=token,
                                isused=False,
                                expired_time=expired_time)
                subject = 'Reset Your Password'
                message = "Hey ," + users.username + \
                    " To reset your password. Your OTP is : " + \
                    str(token)
                email_from = EMAIL_HOST_USER
                recipient_list = [users.email, ]
                send_mail(subject,
                          message,
                          email_from,
                          recipient_list)
                return success_response('OTP sent successfully', 200)
        return error_response(serializer.errors, 400)


class reset_password(APIView):
    def post(self, request):
        if check_forgot_field(request.data):
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']
            username = request.data['username']
            if confirm_password_check(new_password, confirm_password):
                otp = request.data['otp']
                now = int(time.time())
                try:
                    users = User.objects.get(username=username)
                except User.DoesNotExist:
                    return error_response('user not exist', 400)
                user_exist = OTP.objects.get(user=users.id)
                expired_time = user_exist.expired_time
                if now < expired_time:
                    if user_exist.otp == int(otp):
                        user_exist.isused = True
                        user_exist.save()
                        users.password = make_password(new_password)
                        users.save()
                        return success_response("password reset successfully",
                                                200)
                    else:
                        return error_response('OTP expired', 400)
                else:
                    return error_response("OTP expired", 400)
            else:
                return error_response('password not match', 400)
        else:
            return error_response('field(new_password or confirm_password) \
                                  is missing', 400)


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
