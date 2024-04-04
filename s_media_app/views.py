from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from s_media_app.models import User,Post,Like,Comment,Message,Notification
from s_media_app.serializers import (UserSerializer,PostSerializer,LikeSerializer,CommentSerializer,UserProfileSerializer,MessageSerializer,NotificationSerializer)

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

class delete_account(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self,request):
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class get_posts(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class create_post(APIView):
    serializer_class = PostSerializer
    @permission_classes([IsAuthenticated])  
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class update_post(APIView):
    @permission_classes([IsAuthenticated])
    def put(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class delete_post(APIView):
    @permission_classes([IsAuthenticated])
    def delete(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_400_BAD_REQUEST)

class like_post(APIView):
    @permission_classes([IsAuthenticated])
    def post(self,request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)

class comment_on_post(APIView):
    @permission_classes([IsAuthenticated])
    def post(request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class liked_posts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        liked_posts = Post.objects.filter(likes__user=request.user)
        serializer = PostSerializer(liked_posts, many=True)
        return Response(serializer.data)

class commented_posts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        commented_posts = Post.objects.filter(comments__user=request.user)
        serializer = PostSerializer(commented_posts, many=True)
        return Response(serializer.data)

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

class feed(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(user__in=followed_users)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class user_profile(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request, user_id):
        try:
            user_profile = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer =UserProfileSerializer(user_profile)
        return Response(serializer.data)

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
        return Response(serializer.data)

class delete_message(APIView):
    @permission_classes([IsAuthenticated])
    def delete(self,request,sender_id):
        try:
            message = Message.objects.get(sender_id=sender_id, receiver_id=request.user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        Message.delete()
        return Response({'message': 'Message deleted successfully'}, status=status.HTTP_400_BAD_REQUEST)
    


