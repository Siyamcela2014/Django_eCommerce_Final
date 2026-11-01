"""Tests for account registration, login, and password reset."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import ResetToken, UserProfile
from .forms import RegistrationForm

class AccountTests(TestCase):
    """Test important account-related functionality."""

    def test_home_page_loads(self):
        """Check that the home page responds successfully."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        """Check that the login page responds successfully."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_loads(self):
        """Check that the registration page responds successfully."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_registration_rejects_duplicate_email(self):
        """Check that an email address cannot be registered twice."""
        User.objects.create_user(
            username="existingbuyer",
            email="same@example.com",
            password="TestPassword123!",
        )

        form = RegistrationForm(data={
            "username": "newbuyer",
            "email": "same@example.com",
            "password": "TestPassword123!",
            "confirm_password": "TestPassword123!",
            "account_type": "buyer",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_user_can_log_in(self):
        """Check that a registered user can log in."""
        User.objects.create_user(
            username="testbuyer",
            email="buyer@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "testbuyer",
                "password": "TestPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(
                username="testbuyer",
                password="TestPassword123!",
        ))

    def test_reset_token_expires(self):
        """Check that an expired reset token cannot be used."""
        user = User.objects.create_user(
            username="resetbuyer",
            email="resetbuyer@example.com",
            password="TestPassword123!",
        )

        ResetToken.objects.create(
            user=user,
            token="expired-test-token",
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        response = self.client.get(
            reverse(
                "password_reset_confirm",
                args=["expired-test-token"],
            )
        )

        self.assertEqual(response.status_code, 302)