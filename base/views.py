from django.views.generic import TemplateView
from django.shortcuts import render
from menu.models import Dish, Category
from django.db.models.functions import Lower

class HomeView(TemplateView):
    template_name = "base/main_page.html"

def search(request):
    query = request.GET.get("q", "")
    dishes = []
    categories = []

    if query:
        print(query)
        dishes = Dish.objects.annotate(lower_name = Lower('name'))
        print(dishes.first().lower_name)
        dishes = dishes.filter(lower_name__contains=query.lower(), is_available=True)
        categories = Category.objects.filter(name__icontains=query)

    context = {
        "query": query,
        "dishes": dishes,
        "categories": categories,
    }
    return render(request, "base/search_results.html", context)

# def search_dishes_letters(query, dishes):
#     query = query.lower()
#     results = []
#     for dish in dishes:
#         dish_lower = dish.lower()
#         if all(letter in dish_lower for letter in query):
#             results.append(dish)
#     return results