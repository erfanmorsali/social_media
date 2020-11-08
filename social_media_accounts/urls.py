from django.urls import path
from .views import login_page, register_page, log_out, user_dashboard, edit_profile, follow, unfollow

app_name = 'accounts'
urlpatterns = [
    path("accounts/login/", login_page, name='login_page'),
    path("accounts/register/", register_page, name='register_page'),
    path("accounts/logout/", log_out, name='log_out'),
    path("accounts/<int:user_id>/", user_dashboard, name='user_dashboard'),
    path("accounts/edit_profile/<int:user_id>/", edit_profile, name='edit_profile'),
    path("accounts/follow/<int:user_id>/", follow, name="follow"),
    path("accounts/unfollow/<int:user_id>/", unfollow, name="unfollow"),
]
