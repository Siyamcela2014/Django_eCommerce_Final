from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ACCOUNT_TYPES = [
        ("vendor", "Vendor"),
        ("buyer", "Buyer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES
    )

    def __str__(self):
        return f"{self.user.username} - {self.account_type}"

class ResetToken(models.Model):
    """Store a temporary token for resetting a user's password."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        """Return the username associated with this reset token."""
        return f"Password reset token for {self.user.username}"