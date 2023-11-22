from rest_framework import generics
from django.shortcuts import render
from .serializers import *
# Create your views here.
class CommentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()