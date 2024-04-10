from rest_framework import serializers
from s_media_app.error_success_management.error_handler import error_response
from s_media_app.models import User, Post, Like, Comment, Message


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def get_followers(self, obj):
        for follower in obj.followers.all():
            if follower:
                return [follower.username]
            else:
                return error_response('no followers', 400)

    def get_following(self, obj):
        for following in obj.following.all():
            if following:
                return [following.username]
            else:
                return error_response('no following', 400)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'password',
                  'role',
                  'profile_picture',
                  'followers',
                  'following']
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
