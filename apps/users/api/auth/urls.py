from django.urls import path

from knox import views as knox_views

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path(
        "logout-all/", knox_views.LogoutAllView.as_view(),
        name="logout_all",
    ),
    path(
        "password-reset/", views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset-confirm/", views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
