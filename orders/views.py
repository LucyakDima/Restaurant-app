from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect("cart_detail")

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone", "")

        # Перевіряємо, щоб були обов’язкові поля
        if not full_name or not email:
            return render(request, "orders/create_order.html", {
                "cart": cart,
                "error": "Будь ласка, введіть ім'я та електронну пошту."
            })

        # Створюємо замовлення
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            payment_method=payment_method,
        )

        # переносимо товари з кошика в замовлення
        for item in cart.items.all():
            OrderItem.objects.create(order=order, dish=item.dish, quantity=item.quantity)

        cart.items.all().delete()
        return redirect("order_detail", order_id=order.id)

    return render(request, "orders/create_order.html", {"cart": cart})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def repeat_order(request, order_id):
    old_order = get_object_or_404(Order, id=order_id, user=request.user)
    new_order = Order.objects.create(user=request.user)

    for item in old_order.items.all():
        OrderItem.objects.create(
            order=new_order,
            dish=item.dish,
            quantity=item.quantity,
            price=item.price
        )
    return redirect("order_detail", order_id=new_order.id)


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect("order_list")
