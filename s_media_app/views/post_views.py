from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from s_media_app.error_success_management.error_handler import error_response
from s_media_app.error_success_management.success_handler import \
    success_response
from s_media_app.models import Post, Like
from s_media_app.serializers import PostSerializer, LikeSerializer, \
    CommentSerializer


class create_post(APIView):
    serializer_class = PostSerializer

    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return success_response(serializer.data, 201)
        return error_response(serializer.errors, 400)


class get_posts(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return success_response(serializer.data, 202)


class update_post(APIView):
    @permission_classes([IsAuthenticated])
    def put(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
        except Post.DoesNotExist:
            return error_response('Post not found', 404)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, 200)
        return error_response(serializer.errors, 400)


class delete_post(APIView):
    @permission_classes([IsAuthenticated])
    def delete(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
        except Post.DoesNotExist:
            return error_response('Post not found', 404)

        post.delete()
        return success_response('Post deleted successfully', 200)


class like_post(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return error_response('Post not found', 404)
        serializer = LikeSerializer(data=request.data)
        like = Like.objects.get(user=request.user, post=post)
        if like:
            return error_response('You have already liked this post', 208)
        else:
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return success_response('Post liked successfully', 201)
            return error_response(serializer.errors, 400)


class comment_on_post(APIView):
    @permission_classes([IsAuthenticated])
    def post(request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return error_response('Post not found', 404)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return success_response(serializer.data, 201)
        return error_response(serializer.errors, 400)


class liked_posts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        liked_posts = Post.objects.filter(likes__user=request.user). \
            order_by('created_at')
        serializer = PostSerializer(liked_posts, many=True)
        return success_response(serializer.data, 302)


class commented_posts(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        commented_posts = Post.objects.filter(comments__user=request.user). \
            order_by('created_at')
        serializer = PostSerializer(commented_posts, many=True)
        return success_response(serializer.data, 302)


class feed(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(user__in=followed_users). \
            order_by('created_at')
        serializer = PostSerializer(posts, many=True)
        return success_response(serializer.data, 302)
