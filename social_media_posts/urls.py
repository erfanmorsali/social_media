from django.urls import path
from .views import posts_page, post_detail

app_name = 'posts'
urlpatterns = [
    path("all_posts/", posts_page, name='posts_page'),
    path("posts/<int:year>-<int:month>-<int:day>/<slug>", post_detail, name='post_detail'),
]
