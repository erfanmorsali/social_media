from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddPostForm, EditPostForm
from social_media_posts.models import Post
from django.utils.text import slugify


def posts_page(request):
    message = messages.get_messages(request)
    posts = Post.objects.order_by('-created').all()[:10]
    context = {
        "messages": message,
        "posts": posts,
    }
    return render(request, 'social_media_posts/all_posts.html', context)


def post_detail(request, year, month, day, slug):
    message = messages.get_messages(request)
    post = Post.objects.filter(created__year=year, created__month=month, created__day=day, slug=slug).first()
    if post is None:
        return Http404("محصولی با این مشخصات یافت نشد")
    context = {
        "post": post,
        "messages": message,
    }
    return render(request, "social_media_posts/post_detail.html", context)


@login_required(login_url="/accounts/login/")
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


@login_required(login_url="/accounts/login/")
def delete_post_by_user(request, post_id):
    user = get_object_or_404(User, id=request.user.id)
    post = get_object_or_404(Post, id=post_id, user=user).delete()

    messages.success(request, "پست شما با موفقت حذف شد")
    return redirect("accounts:user_dashboard", user.id)


@login_required(login_url="/accounts/login/")
def edit_post_by_user(request, post_id):
    user = get_object_or_404(User, id=request.user.id)
    post = get_object_or_404(Post, id=post_id, user=user)
    form = EditPostForm(request.POST or None, instance=post)
    context = {
        "edit_form": form
    }
    if form.is_valid():
        post.slug = slugify(form.cleaned_data["title"][:30],allow_unicode=True)
        post = form.save()

        messages.success(request, 'تغییرات با موفقت ثبت شد')
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)
    return render(request, "social_media_posts/edit_post.html", context)
