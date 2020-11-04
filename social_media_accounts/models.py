from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user_profile/', null=True, blank=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        user_profile = UserProfile(user=instance)
        user_profile.save()


post_save.connect(create_user_profile, User)
