from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def create_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        return redirect("cart_detail")
    order = Order.objects.create(user=request.user)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            dish=item.dish,
            quantity=item.quantity,
            price=item.dish.price
        )
    cart.items.all().delete()
    return redirect("order_detail", order_id=order.id)


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
