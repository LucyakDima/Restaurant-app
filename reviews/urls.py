from django.urls import path
from .views import add_review, ReviewUpdateView, ReviewDeleteView, ReviewListView

urlpatterns = [
    path("<int:dish_id>/", ReviewListView.as_view(), name="review_list"),
    path("add/<int:dish_id>/", add_review, name="add_review"),
    path("edit/<int:pk>/", ReviewUpdateView.as_view(), name="edit_review"),
    path("delete/<int:pk>/", ReviewDeleteView.as_view(), name="delete_review"),
]
