from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer


class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class FoodCreateView(generics.CreateAPIView):
    serializer_class = FoodSerializer


class FoodUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class FoodListView(generics.ListAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class FoodDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()