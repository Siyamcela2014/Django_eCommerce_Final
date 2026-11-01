"""Tests for products and product reviews."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from stores.models import Store
from .models import Product, Review


class ProductModelTests(TestCase):
    """Test product creation and product details."""

    def setUp(self):
        """Create a user, store, and product for testing."""
        self.user = User.objects.create_user(
            username="testvendor",
            password="TestPassword123!",
        )

        self.store = Store.objects.create(
            owner=self.user,
            name="Test Store",
        )

        self.product = Product.objects.create(
            store=self.store,
            name="Test Laptop",
            description="A laptop for testing.",
            price=Decimal("15000.00"),
            stock_quantity=5,
        )

    def test_product_is_created(self):
        """Confirm that a product is saved correctly."""
        self.assertEqual(self.product.name, "Test Laptop")
        self.assertEqual(self.product.price, Decimal("15000.00"))
        self.assertEqual(self.product.stock_quantity, 5)

    def test_product_string_representation(self):
        """Confirm that a product displays its name."""
        self.assertEqual(str(self.product), "Test Laptop")


class ReviewModelTests(TestCase):
    """Test product review creation and details."""

    def setUp(self):
        """Create a user, store, product, and review."""
        self.user = User.objects.create_user(
            username="testbuyer",
            password="TestPassword123!",
        )

        self.store = Store.objects.create(
            owner=self.user,
            name="Review Test Store",
        )

        self.product = Product.objects.create(
            store=self.store,
            name="Review Test Laptop",
            description="A laptop for review testing.",
            price=Decimal("12000.00"),
            stock_quantity=3,
        )

        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            comment="This product works well.",
            rating=5,
            is_verified=True,
        )

    def test_review_is_created(self):
        """Confirm that the review stores its details."""
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertTrue(self.review.is_verified)

    def test_review_string_representation(self):
        """Confirm that a review displays the product and rating."""
        self.assertEqual(
            str(self.review),
            "Review Test Laptop - 5/5",
        )