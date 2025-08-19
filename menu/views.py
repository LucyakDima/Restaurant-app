from django.views.generic import ListView, DetailView
from .models import Category, Dish
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy


class CategoryListView(ListView):
    model = Category
    template_name = "menu/category_list.html"
    context_object_name = "categories"


class DishListView(ListView):
    model = Dish
    template_name = "menu/dish_list.html"
    context_object_name = "dishes"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Dish.objects.filter(category_id=category_id, is_available=True)


class DishDetailView(DetailView):
    model = Dish
    template_name = "menu/dish_detail.html"
    context_object_name = "dish"


class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dish
    fields = ["category", "name", "description", "price", "is_available", "image"]
    template_name = "menu/dish_edit.html"

    def test_func(self):
        return self.request.user.role == "admin"

    def get_success_url(self):
        return reverse_lazy("dish_detail", kwargs={"pk": self.object.pk})


class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    success_url = reverse_lazy("category_list")

    def test_func(self):
        return self.request.user.role == "admin"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

