from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    age = models.PositiveIntegerField()
    phone = models.IntegerField()
    avatar = models.ImageField(upload_to='user_profile/', null=True, blank=True)
