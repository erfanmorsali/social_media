from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from .models import FollowSystem

# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
admin.site.register(FollowSystem)
