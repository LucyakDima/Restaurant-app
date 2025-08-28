from django.db import models
from django.conf import settings
from menu.models import Dish


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("processing", "В обробці"),
        ("delivered", "Доставлено"),
        ("cancelled", "Скасовано"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return f"Замовлення #{self.id} від {self.user.username} ({self.get_status_display()})"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    def total_price(self):
        return self.price * self.quantity
