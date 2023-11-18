from django.shortcuts import render
import requests

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import IngredientSerializer
from .models import Dish  # Предположим, что у вас есть модель для блюд


class DishCreateView(generics.CreateAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredient_name = serializer.validated_data['products']

        # Далее можно использовать ingredient_name для отправки на ChatGPT и генерации блюда
        # ...
        
        url = "http://127.0.0.1:8000/api/v2/Dish_create/"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",  # Тип контента, может быть другим в зависимости от вашего API
        }

        data = {
            "products": ingredient_name,
            # Дополнительные данные, которые вы хотите отправить в POST-запросе
        }

        response = requests.post(url, headers=headers, json=data)

        print(response.status_code)
        print(response.json())

        # Предположим, что полученный рецепт сохранен в переменной generated_recipe
        user = self.request.user
        dish = Dish(user=user, recipe=response) #заменил generated_recipe на response
        dish.save()

        return Response({"message": "Ingredients received and processed successfully. Dish saved."})
