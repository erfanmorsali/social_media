from django.urls import path
from .views import posts_page, post_detail, add_post_by_user

app_name = 'posts'
urlpatterns = [
    path("all_posts/", posts_page, name='posts_page'),
    path("posts/<int:year>-<int:month>-<int:day>/<slug>/", post_detail, name='post_detail'),
    path("posts/add_post/", add_post_by_user, name='add_post_by_user'),
]
