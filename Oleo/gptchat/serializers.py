from rest_framework import serializers

from .models import Dish

class IngredientSerializer(serializers.Serializer):
    products = serializers.CharField()

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'