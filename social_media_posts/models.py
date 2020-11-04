from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=100, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن پست")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='نام در url')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تبت پست')

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.created.year, self.created.month, self.created.day, self.slug])
