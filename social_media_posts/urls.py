from django.urls import path
from .views import posts_page, post_detail, add_post_by_user, delete_post_by_user, edit_post_by_user, add_reply, \
    like_post, unlike_post

app_name = 'posts'
urlpatterns = [
    path("all_posts/", posts_page, name='posts_page'),
    path("posts/<int:year>-<int:month>-<int:day>/<slug>/", post_detail, name='post_detail'),
    path("posts/add_post/", add_post_by_user, name='add_post_by_user'),
    path("posts/delete_post/<int:post_id>/", delete_post_by_user, name='delete_post_by_user'),
    path("posts/edit_post/<int:post_id>/", edit_post_by_user, name='edit_post_by_user'),
    path("add_reply/<post_id>/<comment_id>/", add_reply, name='add_reply'),
    path("posts/like/<post_id>/", like_post, name='like_post'),
    path("posts/unlike/<post_id>/", unlike_post, name='unlike_post'),
]
