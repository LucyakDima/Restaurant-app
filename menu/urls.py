from django.urls import path
from .views import CategoryListView, DishListView, DishDetailView, DishUpdateView, DishDeleteView

urlpatterns = [
    path('', CategoryListView.as_view(), name="category_list"),
    path('<int:category_id>/', DishListView.as_view(), name="dish_list"),
    path('dish/<int:pk>/', DishDetailView.as_view(), name="dish_detail"),
    path('dish/<int:pk>/edit/', DishUpdateView.as_view(), name="dish_edit"),
    path('dish/<int:pk>/delete/', DishDeleteView.as_view(), name="dish_delete"),
]