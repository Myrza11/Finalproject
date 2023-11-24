from rest_framework import serializers

class IngredientSerializer(serializers.Serializer):
    products = serializers.CharField()