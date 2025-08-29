from django.db import models
from django.conf import settings
from menu.models import Dish

class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(default=5)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Відгук {self.user.username} для {self.dish.name} ({self.rating}★)"
