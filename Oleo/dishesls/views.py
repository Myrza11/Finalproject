from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.none()  # Установите пустой queryset
    permission_classes = [IsAuthenticated]
    #authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class FoodCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer


class FoodUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class FoodListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class FoodDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FoodSerializer
    queryset = Food.objects.all()

