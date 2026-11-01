"""Models for products and customer reviews."""

from django.db import models

from stores.models import Store


class Product(models.Model):
    """Represent a product listed by a vendor in a store."""

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the product name."""
        return self.name


class Review(models.Model):
    """Store a buyer's review and rating for a product."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="product_reviews",
    )
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the product name and rating."""
        return f"{self.product.name} - {self.rating}/5"