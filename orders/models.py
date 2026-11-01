"""Models for customer orders and the products included in each order."""

from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    """Represent an order placed by a buyer."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
    ]

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable description of the order."""
        return f"Order #{self.id} - {self.buyer.username}"


class OrderItem(models.Model):
    """Represent a product and its quantity within an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        """Return the product name and quantity for this order item."""
        return f"{self.product.name} x {self.quantity}"