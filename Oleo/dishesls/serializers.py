
from django.db.models import fields
from rest_framework import serializers
from .models import *




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        
class ComentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coment
        fields = '__all__'