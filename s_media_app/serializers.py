from rest_framework import serializers
from s_media_app.models import User,Post,Like,Comment,Message,Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}
class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    def get_followers(self, obj):
        return [follower.username for follower in obj.followers.all()]

    def get_following(self, obj):
        return [following.username for following in obj.following.all()]

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'followers', 'following']
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
class NotificationSerializer(serializers.Serializer):
    class Meta:
        mpdel=Notification
        fields='__all__'