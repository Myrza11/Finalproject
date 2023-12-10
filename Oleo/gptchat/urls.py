from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *


urlpatterns = [
    path('dish-create/', DishCreateView.as_view()),
    path('dish-list/', DishListView.as_view()),
    path('dish-destroy/', FoodDestroyView.as_view()),
    path('image/<str:image_url>/', ImageView.as_view()),
    ]
