from rest_framework import serializers
from social_media_posts.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=True, allow_null=False, allow_blank=False)
    body = serializers.CharField(max_length=500, required=True, allow_null=False, allow_blank=False)
    user_id = serializers.IntegerField(required=True, allow_null=False)


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, required=True, allow_null=False, allow_blank=False)
    body = serializers.CharField(max_length=500, required=True, allow_null=False, allow_blank=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_login",
            "is_superuser",
            "username",
            "email",
            "date_joined",
        )
