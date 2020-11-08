from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db.models import Q


# Create your models here.
class PostManager(models.Manager):
    def search(self, key):
        lookup = (
                Q(title__icontains=key) |
                Q(body__icontains=key) |
                Q(user__username__icontains=key)
        )
        return self.get_queryset().filter(lookup).distinct()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=100, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن پست")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name='نام در url')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تبت پست')
    objects = PostManager()

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.user.username + '--' + self.title[:30]

    def get_absolute_url(self):
        return reverse("posts:post_detail", args=[self.created.year, self.created.month, self.created.day, self.slug])

    def like_count(self):
        return self.post_likes.count()


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomment", verbose_name='کاربر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcomment', verbose_name='پست')
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='replycomment',
                              verbose_name="ریپلای")
    is_reply = models.BooleanField(default=False, verbose_name='ریپلای شده')
    body = models.TextField(max_length=400, verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'کامنت',
        verbose_name_plural = 'کامنت ها'
        ordering = ('-created',)


class LikeSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.username + " ---> " + self.post.title
