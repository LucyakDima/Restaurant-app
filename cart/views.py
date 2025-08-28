from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import Dish
from .models import Cart, ItemInCart

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

@login_required
def add_to_cart(request, dish_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    dish = get_object_or_404(Dish, id=dish_id)
    item, created = ItemInCart.objects.get_or_create(cart=cart, dish=dish)
    if not created:
        item.quantity += 1
        item.save()
    return redirect(request.META.get("HTTP_REFERER", "cart_detail"))


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(ItemInCart, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart_detail")


@login_required
def update_quantity(request, item_id, action):
    item = get_object_or_404(ItemInCart, id=item_id, cart__user=request.user)
    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect("cart_detail")