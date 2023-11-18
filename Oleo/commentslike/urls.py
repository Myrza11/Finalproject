from django.urls import path
from .views import *



urlpatterns = [
    path('create_coment/', CommentCreateView.as_view()),
    path('update_coment/<int:pk>', CommentUpdateView.as_view()),
    path('list_coment/', CommentListView.as_view()),
    path('destroy_coment/<int:pk>', CommentDestroyView.as_view()),
    ]