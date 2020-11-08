from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import AllPosts, PostDetail, PostCreate, UpdatePost, SearchPost, PostDelete, AllUsers, UserProfile, \
    UserDetail, UserDelete

app_name = 'apis'
urlpatterns = [
    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # posts
    path("api/v1/posts/all_data/", AllPosts.as_view()),
    path("api/v1/posts/<int:post_id>/", PostDetail.as_view()),
    path("api/v1/posts/post_create/", PostCreate.as_view()),
    path("api/v1/posts/update/<int:post_id>/", UpdatePost.as_view()),
    path("api/v1/posts/search", SearchPost.as_view()),
    path("api/v1/posts/delete/<int:post_id>/", PostDelete.as_view()),
    # users
    path('api/v1/users/all_data/', AllUsers.as_view()),
    path('api/v1/users/profile/', UserProfile.as_view()),
    path('api/v1/users/<int:user_id>/', UserDetail.as_view()),
    path('api/v1/users/delete/<int:user_id>/', UserDelete.as_view()),
]
