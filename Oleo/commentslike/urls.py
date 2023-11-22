from django.urls import path
from .views import *



urlpatterns = [
    path('create/', CommentCreateView.as_view()),
    path('update/<int:pk>', CommentUpdateView.as_view()),
    path('list/', CommentListView.as_view()),
    path('destroy/<int:pk>', CommentDestroyView.as_view()),
    path('detail/<int:pk>', CommentDetailView.as_view())
    ]