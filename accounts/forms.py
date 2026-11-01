from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    """Form for registering buyers and vendors."""

    ACCOUNT_TYPES = [
        ("vendor", "Vendor"),
        ("buyer", "Buyer"),
    ]

    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    confirm_password = forms.CharField(
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPES,
        label="Account Type",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = User
        fields = ["username", "email"]

        field_order = [
            "username",
            "email",
            "password",
            "confirm_password",
            "account_type",
        ]

    def clean(self):
        """Validate that the password fields match."""
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if (
            password
            and confirm_password
            and password != confirm_password
        ):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        """Save the user with an email address and hashed password."""
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user

    def clean_email(self):
        """Prevent duplicate email addresses during registration."""
        email = self.cleaned_data.get("email")

        if email:
            existing_email = User.objects.filter(
                email__iexact=email
            )

            if self.instance.pk:
                existing_email = existing_email.exclude(
                    pk=self.instance.pk
                )

            if existing_email.exists():
                raise forms.ValidationError(
                    "An account with this email address already exists."
                )

        return email
