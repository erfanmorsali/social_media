from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddPostForm, EditPostForm, PostCommentForm, AddReplyForm
from social_media_posts.models import Post, PostComment, LikeSystem
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
    reply_form = AddReplyForm(request.POST or None)
    form = PostCommentForm(request.POST or None)
    post = get_object_or_404(Post, created__year=year, created__month=month, created__day=day, slug=slug)
    global liked_by_user
    liked_by_user = False
    if request.user.is_authenticated:
        is_like = LikeSystem.objects.filter(user=request.user, post=post)
        if is_like.exists():
            liked_by_user = True
    comments = PostComment.objects.filter(post=post, is_reply=False)
    context = {
        "post": post,
        "messages": message,
        "comments": comments,
        "comment_form": form,
        "reply_form": reply_form,
        "is_like": liked_by_user
    }
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = post
        new_comment.save()
        context["comment_form"] = PostCommentForm()
        messages.success(request, "کامنت شما با موفقیت ثبت شد")
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day, post.slug)
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
        post.slug = slugify(form.cleaned_data["title"][:30], allow_unicode=True)
        post = form.save()

        messages.success(request, 'تغییرات با موفقت ثبت شد')
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)
    return render(request, "social_media_posts/edit_post.html", context)


@login_required(login_url="/accounts/login/")
def add_reply(request, post_id, comment_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(PostComment, id=comment_id)
    reply_form = AddReplyForm(request.POST or None)
    if reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.post = post
        reply.user = user
        reply.is_reply = True
        reply.reply = comment
        reply.save()
        messages.success(request, "نظر شما با موفقیت ثبت شد")
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)


@login_required(login_url='/accounts/login/')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_like = LikeSystem.objects.filter(user=user, post=post)
    if is_like.exists():
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)
    else:
        LikeSystem(user=user, post=post).save()
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)


@login_required(login_url='/accounts/login/')
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    is_like = LikeSystem.objects.filter(user=user, post=post)
    if is_like.exists():
        is_like.delete()
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)

    else:
        return redirect("posts:post_detail", post.created.year, post.created.month, post.created.day,
                        post.slug)
