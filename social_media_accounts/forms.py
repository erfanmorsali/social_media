from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", "placeholder": "نام کاربری خود را وارد کنید"})
                               )
    password = forms.CharField(label='کلمه ی عبور',
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control", "placeholder": "کلمه ی عبور خود را وارد کنید"}))


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", "placeholder": "نام کاربری خود را وارد کنید"})
                               )

    email = forms.EmailField(max_length=100,

                             widget=forms.EmailInput(
                                 attrs={"class": "form-control", "placeholder": " ایمیل عبور خود را وارد کنید"}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "کلمه ی عبور خود را وارد کنید"}))

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "کلمه ی عبور خود را وارد کنید"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("کاربری با این ایمیل در سایت موجود میباشد")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("کاربری با این نام کاربری در سایت موجود میباشد")

        return username

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password2 != password:
            raise forms.ValidationError("کلمه های عبور مغایرت دارند")
        return password2
