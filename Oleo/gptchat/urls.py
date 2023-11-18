from django.urls import path
from .views import *

urlpatterns = [
    path('Dish_create/', DishCreateView.as_view()),
    ]