from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddPostForm
from social_media_posts.models import Post
from django.utils.text import slugify


def posts_page(request):
    message = messages.get_messages(request)
    posts = Post.objects.all()[:10]
    context = {
        "messages": message,
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


def add_post_by_user(request):
    user = get_object_or_404(User, id=request.user.id)
    form = AddPostForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = user
        new_post.slug = slugify(new_post.title[:30], allow_unicode=True)
        new_post.save()
        messages.success(request, "پست با موفقیت ایجاد شد")
        return redirect("accounts:user_dashboard", user.id)
    return render(request, 'social_media_posts/add_post.html', context)
