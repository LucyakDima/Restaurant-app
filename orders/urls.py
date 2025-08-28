from django.urls import path
from .views import *

urlpatterns = [
    path("create/", create_order, name="create_order"),
    path("<int:order_id>/", order_detail, name="order_detail"),
    path("<int:order_id>/repeat/", repeat_order, name="repeat_order"),
    path("<int:order_id>/delete/", delete_order, name="delete_order"),
    path("", order_list, name="order_list"),
]
