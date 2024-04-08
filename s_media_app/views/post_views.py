from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from s_media_app.models import Post,Like
from s_media_app.serializers import PostSerializer,LikeSerializer,CommentSerializer

class create_post(APIView):
    serializer_class = PostSerializer
    @permission_classes([IsAuthenticated])  
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class get_posts(APIView):
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

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
        serializer = LikeSerializer(data=request.data)
        like = Like.objects.get(user=request.user, post=post)
        if like:
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        liked_posts = Post.objects.filter(likes__user=request.user).order_by('created_at')
        serializer = PostSerializer(liked_posts, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)

class commented_posts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        commented_posts = Post.objects.filter(comments__user=request.user).order_by('created_at')
        serializer = PostSerializer(commented_posts, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)

class feed(APIView):
    @permission_classes([IsAuthenticated])
    def get(self,request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(user__in=followed_users).order_by('created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)