from django.db import models
from django.conf import settings
from menu.models import Dish

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return f"Кошик {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class ItemInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    def total_price(self):
        return self.dish.price * self.quantity