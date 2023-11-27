from django.shortcuts import render
import requests

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import IngredientSerializer
from .models import Dish  # Предположим, что у вас есть модель для блюд


'''class DishCreateView(generics.CreateAPIView):
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
        print(response.text)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")
            print(response.text) 

        print(response.status_code)
        print(response.json())

        # Предположим, что полученный рецепт сохранен в переменной generated_recipe
        user = self.request.user
        dish = Dish(user=user, recipe=response) #заменил generated_recipe на response
        dish.save()

        return Response({"message": "Ingredients received and processed successfully. Dish saved."})'''

class DishCreateView(generics.CreateAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def generate_dish(self, ingredient_name):
        url = "http://127.0.0.1:8000/api/v2/Dish_create/"
        headers = {
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        }
        data = {"products": ingredient_name}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Error in generating dish: {str(e)}"}

    def save_dish(self, user, recipe):
        dish = Dish(user=user, recipe=recipe)
        dish.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredient_name = serializer.validated_data['products']

        generated_recipe = self.generate_dish(ingredient_name)

        if "error" in generated_recipe:
            return Response({"error": generated_recipe["error"]}, status=500)

        self.save_dish(request.user, generated_recipe)

        return Response({"message": "Ingredients received and processed successfully. Dish saved."})
