from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView, ListView
from .forms import ReviewForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from menu.models import Dish

@login_required
def add_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if Review.objects.filter(user=request.user, dish=dish).exists():
        messages.error(request, "Ви вже залишали відгук для цієї страви.")
        return redirect("review_list", dish_id=dish.id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.dish = dish
            review.save()
            messages.success(request, "Ваш відгук успішно додано!")
            return redirect("review_list", dish_id=dish.id)
    else:
        form = ReviewForm()
    return render(request, "reviews/add_review.html", {"form": form, "dish": dish})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/edit_review.html"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse_lazy("dish_detail", kwargs={"pk": self.object.dish.id})


@method_decorator(login_required, name="dispatch")
class ReviewListView(ListView):
    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        self.dish = Dish.objects.get(id=self.kwargs["dish_id"])
        return Review.objects.filter(dish=self.dish)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = self.dish
        return context


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "reviews/delete_review.html"
    success_url = reverse_lazy("category_list")

    def test_func(self):
        return self.request.user.is_superuser or self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse_lazy("dish_detail", kwargs={"pk": self.object.dish.id})
