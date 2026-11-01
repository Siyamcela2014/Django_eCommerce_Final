"""Views for creating, editing, and deleting vendor stores."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StoreForm
from .models import Store


@login_required
def create_store(request):
    """Create a store owned by the currently logged-in vendor."""
    if request.method == "POST":
        form = StoreForm(request.POST)

        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()

            return redirect("vendor_dashboard")
    else:
        form = StoreForm()

    return render(
        request,
        "stores/create_store.html",
        {"form": form}
    )


@login_required
def edit_store(request, store_id):
    """Edit a store only if it belongs to the current user."""
    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)

        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = StoreForm(instance=store)

    return render(
        request,
        "stores/edit_store.html",
        {"form": form, "store": store}
    )


@login_required
def delete_store(request, store_id):
    """Delete a store only if it belongs to the current user."""
    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == "POST":
        store.delete()
        return redirect("vendor_dashboard")

    return render(
        request,
        "stores/delete_store.html",
        {"store": store}
    )