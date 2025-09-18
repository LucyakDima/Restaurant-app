from django.db import models
from django.conf import settings
from menu.models import Dish


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("card", "Оплата карткою"),
        ("cash", "Оплата при отриманні"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="cash")
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    def total_price(self):
        return self.dish.price * self.quantity

