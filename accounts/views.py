"""Views for account registration, authentication, dashboards, and password resets."""

from datetime import timedelta
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import RegistrationForm
from .models import ResetToken, UserProfile


def register(request):
    """Register a buyer or vendor and redirect to the appropriate dashboard."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(
                user=user,
                account_type=form.cleaned_data["account_type"],
            )

            login(request, user)

            if form.cleaned_data["account_type"] == "vendor":
                return redirect("vendor_dashboard")

            return redirect("buyer_dashboard")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


def home(request):
    """Display the account home page."""
    return render(request, "accounts/home.html")


@login_required
def vendor_dashboard(request):
    """Display the stores and products belonging to the logged-in vendor."""
    from stores.models import Store

    stores = Store.objects.filter(
        owner=request.user
    ).prefetch_related("products")

    return render(
        request,
        "accounts/home.html",
        {"stores": stores},
    )


@login_required
def buyer_dashboard(request):
    """Display available products to the logged-in buyer."""
    from products.models import Product

    products = Product.objects.select_related("store").all()

    return render(
        request,
        "accounts/buyer_dashboard.html",
        {"products": products},
    )


def user_login(request):
    """Authenticate a user and redirect according to their account type."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            profile = UserProfile.objects.filter(user=user).first()

            if profile is None:
                messages.error(
                    request,
                    "Your account profile could not be found.",
                )
                logout(request)
                return redirect("login")

            if profile.account_type == "vendor":
                return redirect("vendor_dashboard")

            return redirect("buyer_dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(request, "accounts/login.html")


def user_logout(request):
    """Log out the current user and redirect to the login page."""
    logout(request)
    return redirect("login")


def password_reset_request(request):
    """Create a time-limited password-reset token for a registered email."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token = uuid4().hex

            ResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=1),
            )

            reset_link = request.build_absolute_uri(
                f"/accounts/password-reset-confirm/{token}/"
            )

            messages.success(
                request,
                f"Password reset link (development only): {reset_link}",
            )
        else:
            messages.success(
                request,
                "If that email address is registered, "
                "a password reset link will be provided.",
            )

        return redirect("password_reset_request")

    return render(request, "accounts/password_reset.html")


def password_reset_confirm(request, token):
    """Validate a reset token and securely update the user's password."""
    reset_token = ResetToken.objects.filter(
        token=token,
        used=False,
        expires_at__gt=timezone.now(),
    ).select_related("user").first()

    if reset_token is None:
        messages.error(
            request,
            "This password reset link is invalid or expired.",
        )
        return redirect("password_reset_request")

    if request.method == "POST":
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not password or len(password) < 8:
            messages.error(
                request,
                "Your new password must contain at least 8 characters.",
            )
        elif password != confirm_password:
            messages.error(
                request,
                "The passwords do not match.",
            )
        else:
            user = reset_token.user
            user.set_password(password)
            user.save()

            reset_token.used = True
            reset_token.save(update_fields=["used"])

            messages.success(
                request,
                "Your password has been reset successfully. "
                "Please log in with your new password.",
            )
            return redirect("login")

    return render(
        request,
        "accounts/password_reset_confirm.html",
    )