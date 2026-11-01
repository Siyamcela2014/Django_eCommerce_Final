"""URL configuration for the eCommerce project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="browse_products", permanent=False)),
    path("accounts/", include("accounts.urls")),
    path("stores/", include("stores.urls")),
    path("products/", include("products.urls")),
]