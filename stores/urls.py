from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_store, name="create_store"),
    path("edit/<int:store_id>/", views.edit_store, name="edit_store"),
    path("delete/<int:store_id>/", views.delete_store, name="delete_store"),
]