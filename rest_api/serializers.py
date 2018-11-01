from django.contrib.auth.models import User
from groups.models import Group
from posts.models import Post
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest_api:user-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('name', 'slug', 'description', 'members', 'image')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(many=False)
    group = serializers.StringRelatedField(many=False)

    class Meta:
        model = Post
        fields = ('user', 'created_at', 'message', 'group', 'image')
