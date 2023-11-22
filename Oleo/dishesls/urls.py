from django.urls import path
from .views import *

urlpatterns = [
    path('create-category/', CategoryCreateView.as_view()),
    path('update-category/<int:pk>', CategoryUpdateView.as_view()),
    path('list-category/', CategoryListView.as_view()),
    path('destroy-category/<int:pk>', CategoryDestroyView.as_view()),
    path('create-food/', FoodCreateView.as_view()),
    path('update-food/<int:pk>', FoodUpdateView.as_view()),
    path('list-food/', FoodListView.as_view()),
    path('destroy-food/<int:pk>', FoodDestroyView.as_view()),


]