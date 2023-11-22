from django.urls import path
from .views import *

urlpatterns = [
    path('dish-create/', DishCreateView.as_view()),
    ]