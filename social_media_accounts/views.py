from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from social_media_posts.models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.


def login_page(request):
    next_page = request.GET.get("next")
    login_form = LoginForm(request.POST or None)
    messsage = messages.get_messages(request)
    context = {
        "login_form": login_form,
        "messages": messsage
    }
    if login_form.is_valid():
        cd = login_form.cleaned_data
        user = authenticate(request, username=cd["username"], password=cd['password'])
        if user is not None:
            login(request, user)
            messages.success(request, "شما با موفقیت وارد شدید")
            context["login_form"] = LoginForm()
            if next_page is not None:
                return redirect(next_page)
            else:
                return redirect("posts:posts_page")
        else:
            login_form.add_error("username", "کاربری با این مشخصات یافت نشد")

    return render(request, "accounts/login_page.html", context)


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        "register_form": register_form
    }

    if register_form.is_valid():
        cd = register_form.cleaned_data
        user = User.objects.create_user(cd["username"], cd["email"], cd['password'])
        messages.success(request, 'شما با موفقیت ثبت نام کردید')
        login(request, user)
        return redirect("posts:posts_page")
    return render(request, "accounts/register_page.html", context)


@login_required(login_url="/accounts/login/")
def log_out(request):
    logout(request)
    messages.success(request, "شما با موفقت خارج شدید")
    return redirect("posts:posts_page")


@login_required(login_url="/accounts/login/")
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    message = messages.get_messages(request)
    posts = Post.objects.filter(user=user)
    context = {
        "user": user,
        "posts": posts,
        "messages": message,
    }
    return render(request, "accounts/user_dashboard.html", context)



