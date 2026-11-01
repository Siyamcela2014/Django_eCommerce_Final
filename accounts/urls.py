from django.urls import path

from .views import (
    home,
    register,
    vendor_dashboard,
    buyer_dashboard,
    user_login,
    user_logout,
    password_reset_request,
    password_reset_confirm,
)


urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path(
        "vendor-dashboard/",
        vendor_dashboard,
        name="vendor_dashboard",
    ),
    path(
        "buyer-dashboard/",
        buyer_dashboard,
        name="buyer_dashboard",
    ),

    path("password-reset/", password_reset_request, name="password_reset_request"),
    path("password-reset-confirm/<str:token>/", password_reset_confirm, name="password_reset_confirm"),
]