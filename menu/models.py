from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import Sum
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        return self.name


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Формат зображення не підтримується. Використовуйте JPG, PNG або WEBP.')

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True, validators=[MinLengthValidator(4)])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="dishes/", blank=True, null=True, validators=[validate_image_extension])


    def __str__(self):
        return f"{self.name} - {self.price} грн"

    def orders_count(self):
        return self.orderitem_set.aggregate(total=Sum("quantity"))["total"] or 0