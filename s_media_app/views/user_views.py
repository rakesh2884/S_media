from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from s_media_app.decorators import is_admin
from s_media_app.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from s_media_app.serializers import UserSerializer

class register(APIView):
    serializer_class = UserSerializer
    def post(self,request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save(password=make_password(request.data['password']))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class login(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class get_profile(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class update_profile(APIView):
    @permission_classes([IsAuthenticated])
    def put(self,request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class delete_self_account(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({'message': 'Your account deleted successfully'}, status=status.HTTP_202_ACCEPTED)

class user_profile(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request, user_id):
        try:
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer =UserSerializer(user_profile)
        return Response(serializer.data,status=status.HTTP_302_FOUND)