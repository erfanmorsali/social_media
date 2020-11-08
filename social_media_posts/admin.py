from django.contrib import admin
from .models import Post, PostComment,LikeSystem


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'title', "slug", "created")


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'post', "created")


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment,PostCommentAdmin)
admin.site.register(LikeSystem)
