from django.urls import path
from .views import login_page, register_page, log_out, user_dashboard

app_name = 'accounts'
urlpatterns = [
    path("accounts/login/", login_page, name='login_page'),
    path("accounts/register/", register_page, name='register_page'),
    path("accounts/logout/", log_out, name='log_out'),
    path("accounts/<int:user_id>/", user_dashboard, name='user_dashboard'),

]
