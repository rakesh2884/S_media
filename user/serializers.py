from rest_framework import serializers
from utils.error_handler import error_response
from user.models import User, Link


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
                  'following',
                  'login_attempt'
                  ]
        extra_kwargs = {'password': {'write_only': True},
                        'login_attempt': {'write_only': True}}


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
