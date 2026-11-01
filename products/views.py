"""Views for product management, shopping carts, checkout, and reviews."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from stores.models import Store
from .models import Product, Review
from .forms import ProductForm


# =========================
# VENDOR PRODUCT FUNCTIONS
# =========================

@login_required
def create_product(request, store_id):
    """Create a product in a store owned by the current vendor."""
    store = get_object_or_404(
        Store,
        id=store_id,
        owner=request.user
    )

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()

            return redirect("vendor_dashboard")
    else:
        form = ProductForm()

    return render(
        request,
        "products/create_product.html",
        {"form": form, "store": store}
    )


@login_required
def edit_product(request, product_id):
    """Edit a product belonging to the current vendor."""
    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user
    )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("vendor_dashboard")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/edit_product.html",
        {"form": form, "product": product}
    )


@login_required
def delete_product(request, product_id):
    """Delete a product belonging to the current vendor."""
    product = get_object_or_404(
        Product,
        id=product_id,
        store__owner=request.user
    )

    if request.method == "POST":
        product.delete()
        return redirect("vendor_dashboard")

    return render(
        request,
        "products/delete_product.html",
        {"product": product}
    )


# =========================
# BUYER PRODUCT FUNCTIONS
# =========================

@login_required
def browse_products(request):
    """Display the products available for browsing."""
    products = Product.objects.select_related("store").all()

    return render(
        request,
        "products/browse_products.html",
        {"products": products}
    )


@login_required
def add_to_cart(request, product_id):
    """Add a selected product quantity without exceeding available stock."""
    product = get_object_or_404(Product, id=product_id)

    if request.method != "POST":
        return redirect("browse_products")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Please enter a valid quantity.")
        return redirect("browse_products")

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("browse_products")

    cart = request.session.get("cart", {})
    product_id_string = str(product_id)

    current_quantity = cart.get(product_id_string, 0)
    new_quantity = current_quantity + quantity

    if new_quantity > product.stock_quantity:
        messages.error(
            request,
            f"Only {product.stock_quantity} units of "
            f"{product.name} are available. "
            f"You already have {current_quantity} in your cart."
        )
        return redirect("view_cart")

    cart[product_id_string] = new_quantity
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{quantity} unit(s) of {product.name} added to your cart."
    )

    return redirect("view_cart")


@login_required
def view_cart(request):
    """Display the shopping cart and calculate its total."""
    cart = request.session.get("cart", {})

    cart_items = []
    total_amount = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total_amount += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "products/cart.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
        }
    )


@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the shopping cart."""
    cart = request.session.get("cart", {})

    product_id_string = str(product_id)

    if product_id_string in cart:
        del cart[product_id_string]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("view_cart")

@login_required
def clear_cart(request):
    """Remove all products from the buyer's shopping cart."""
    if request.method == "POST":
        request.session["cart"] = {}
        request.session.modified = True

        messages.success(
            request,
            "Your shopping cart has been cleared."
        )

    return redirect("view_cart")


@login_required
def checkout(request):
    """Create an order, update stock, and generate an invoice email."""
    from django.core.mail import send_mail
    from django.conf import settings
    from django.contrib import messages
    from django.shortcuts import redirect, render
    from orders.models import Order, OrderItem

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("view_cart")

    # Check stock and calculate the order total before creating the order.
    total_amount = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        if quantity > product.stock_quantity:
            messages.error(
                request,
                f"Not enough stock available for {product.name}."
            )
            return redirect("view_cart")

        total_amount += product.price * quantity

    # Create the order.
    order = Order.objects.create(
        buyer=request.user,
        total_amount=total_amount,
        status="completed",
    )

    # Build the invoice and create order items.
    invoice_lines = [
        f"Invoice for Order #{order.id}",
        f"Customer: {request.user.username}",
        "",
        "Purchased items:",
    ]

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
        )

        product.stock_quantity -= quantity
        product.save()

        invoice_lines.append(
            f"{product.name} | "
            f"Quantity: {quantity} | "
            f"Unit price: R{product.price} | "
            f"Subtotal: R{subtotal}"
        )

    invoice_lines.extend([
        "",
        f"Order total: R{total_amount}",
        "",
        "Thank you for shopping with us!",
    ])

    invoice_message = "\n".join(invoice_lines)

    # Email the invoice to the buyer.
    if request.user.email:
        send_mail(
            subject=f"Invoice for Order #{order.id}",
            message=invoice_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        messages.success(
            request,
            f"Your invoice for Order #{order.id} has been generated."
        )
    else:
        messages.warning(
            request,
            "Your order was created, but no invoice email was sent "
            "because your account has no email address."
        )

    # Clear the cart after successful checkout.
    request.session["cart"] = {}
    request.session.modified = True

    return render(
        request,
        "products/checkout.html",
        {"order": order}
    )


@login_required
def add_review(request, product_id):
    """Submit a product review and identify verified purchases."""
    product = get_object_or_404(Product, id=product_id)

    from orders.models import OrderItem

    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        rating = request.POST.get("rating", "")

        try:
            rating = int(rating)
        except (TypeError, ValueError):
            rating = 0

        if not comment:
            messages.error(
                request,
                "Please enter a review comment."
            )
        elif rating < 1 or rating > 5:
            messages.error(
                request,
                "Please select a rating between 1 and 5."
            )
        else:
            is_verified = OrderItem.objects.filter(
                order__buyer=request.user,
                order__status="completed",
                product=product
            ).exists()

            Review.objects.create(
                product=product,
                user=request.user,
                comment=comment,
                rating=rating,
                is_verified=is_verified
            )

            if is_verified:
                messages.success(
                    request,
                    "Your review has been submitted as a verified purchase."
                )
            else:
                messages.success(
                    request,
                    "Your review has been submitted as an unverified purchase."
                )

        return redirect("browse_products")

    return render(
        request,
        "products/add_review.html",
        {"product": product}
    )