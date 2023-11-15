from django.urls import path
from .views import *

urlpatterns = [
    path('create_category/', CategoryCreateView.as_view()),
    path('update_category/<int:pk>', CategoryUpdateView.as_view()),
    path('list_category/', CategoryListView.as_view()),
    path('destroy_category/<int:pk>', CategoryDestroyView.as_view()),
    path('create_food/', FoodCreateView.as_view()),
    path('update_food/<int:pk>', FoodUpdateView.as_view()),
    path('list_food/', FoodListView.as_view()),
    path('destroy_food/<int:pk>', FoodDestroyView.as_view()),
 
]