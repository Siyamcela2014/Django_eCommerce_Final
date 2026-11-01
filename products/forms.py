from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "e.g. 199.99",
            }
        ),
    )

    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock_quantity"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "stock_quantity": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
        }