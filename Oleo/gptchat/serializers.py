from rest_framework import serializers

from .models import Dish

class IngredientSerializer(serializers.Serializer):
    products = serializers.CharField()
    exceptions = serializers.CharField()
    wishes = serializers.CharField()
    class Meta:
        fields = 'products exceptions wishes'.split()

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'