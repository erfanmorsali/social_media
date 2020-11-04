from django.contrib import messages
from django.http import Http404
from django.shortcuts import render

from social_media_posts.models import Post


def posts_page(request):
    message = messages.get_messages(request)
    posts = Post.objects.all()[:10]
    context = {
        "messages" : message,
        "posts": posts,
    }
    return render(request, 'social_media_posts/all_posts.html', context)


def post_detail(request, year, month, day, slug):
    post = Post.objects.filter(created__year=year, created__month=month, created__day=day, slug=slug).first()
    if post is None:
        return Http404("محصولی با این مشخصات یافت نشد")
    context = {
        "post": post
    }
    return render(request, "social_media_posts/post_detail.html", context)
