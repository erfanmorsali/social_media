from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, UserSerializer
from social_media_posts.models import Post
from rest_framework import status, permissions
from django.utils.text import slugify


class AllPosts(APIView):
    def get(self, request):
        try:
            query = Post.objects.order_by('-created').all()[:20]
            data = []
            for info in query:
                data.append({
                    "id": info.id,
                    "title": info.title,
                    "body": info.body[:60],
                    "created": info.created.date(),
                    "user": info.user.username
                })
            return Response(data, status.HTTP_200_OK)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetail(APIView):
    def get(self, request, post_id):
        try:
            query = Post.objects.get(id=post_id)
            serializer = PostSerializer(query)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"data": "not found"}, status.HTTP_404_NOT_FOUND)


class PostCreate(APIView):
    def post(self, request):
        try:
            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                cd = serializer.data
            else:
                return Response({"data": "somethings wrong"}, status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=cd["user_id"])
            new_post = Post()
            new_post.title = cd["title"]
            new_post.body = cd["body"]
            new_post.slug = slugify(cd["title"][:30], allow_unicode=True)
            new_post.user = user
            new_post.save()
            return Response({"data": new_post.title}, status.HTTP_201_CREATED)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePost(APIView):
    def put(self, request, post_id):
        try:
            serializer = PostUpdateSerializer(data=request.data)
            if serializer.is_valid():
                cd = serializer.data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            post = Post.objects.get(id=post_id, user=request.user)
            post.title = cd["title"]
            post.body = cd["body"]
            post.slug = slugify(cd["title"][:30], allow_unicode=True)
            post.save()
            return Response({"data": post.title}, status.HTTP_202_ACCEPTED)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDelete(APIView):
    def delete(self, request, post_id):
        try:
            query = Post.objects.get(id=post_id, user=request.user)
            query.delete()
            return Response({"data": request.user.username}, status.HTTP_202_ACCEPTED)

        except:
            return Response({"data": "somethings wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchPost(APIView):
    def get(self, request):
        try:
            key = request.GET.get('q')
            query = Post.objects.search(key)
            serializer = PostSerializer(query, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"data": "not found"}, status.HTTP_404_NOT_FOUND)


class AllUsers(APIView):
    def get(self, request):
        try:
            query = User.objects.all()[:20]
            serializer = UserSerializer(query, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfile(APIView):

    def get(self, request):
        try:
            query = request.user
            serializer = UserSerializer(query)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, user_id):
        try:
            query = User.objects.get(id=user_id)
            serializer = UserSerializer(query)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, user_id):
        try:
            query = User.objects.get(id=user_id)
            query.delete()
            return Response({"data": "deleted"}, status.HTTP_202_ACCEPTED)
        except:
            return Response({"data": "somethings wrong"}, status.HTTP_400_BAD_REQUEST)
