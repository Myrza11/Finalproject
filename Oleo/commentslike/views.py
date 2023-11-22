from rest_framework import generics
from django.shortcuts import render
from .serializers import *
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class CommentUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    #authentication_classes = [JWTAuthentication]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        # Set the user before saving the comment
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()