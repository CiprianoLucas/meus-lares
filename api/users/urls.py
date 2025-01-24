from allauth.account import views
from django.conf import settings
from django.urls import path, re_path
from django.views.generic.base import RedirectView

from .views import (
    GoogleLogin,
    LoginView,
    UserCreateView,
    get_info,
    logout_view,
    roles_view,
)

urlpatterns = [
    path("info/", get_info, name="csrf"),
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("google-login/", GoogleLogin.as_view(), name="google_login_by_token"),
    path("logout/", logout_view, name="logout"),
    path("roles/", roles_view, name="roles"),
    path(
        "f/confirm-email/",
        views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    path(
        "f/signup/",
        RedirectView.as_view(url=settings.LOGOUT_REDIRECT_URL),
        name="account_signup",
    ),
    re_path(
        r"^f/confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
    path("f/password/reset/", views.password_reset, name="account_reset_password"),
    path(
        "f/password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(
        r"^f/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.password_reset_from_key,
        name="account_reset_password_from_key",
    ),
    path(
        "f/password/reset/key/done/",
        views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
    path(
        "f/login/code/confirm/",
        views.confirm_login_code,
        name="account_confirm_login_code",
    ),
]
