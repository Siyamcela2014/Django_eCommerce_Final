from django.urls import path

from . import views


urlpatterns = [
    path(
        "create/<int:store_id>/",
        views.create_product,
        name="create_product",
    ),
    path(
        "edit/<int:product_id>/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "delete/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
    path(
        "browse/",
        views.browse_products,
        name="browse_products",
    ),
    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/",
        views.view_cart,
        name="view_cart",
    ),
        path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path(
        "clear-cart/",
        views.clear_cart,
        name="clear_cart",
    ),
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
    path(
        "review/<int:product_id>/",
        views.add_review,
        name="add_review",
    ),
]