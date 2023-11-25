from django.urls import path, include
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', CustomUserLoginView.as_view()), 
    path('change-password/', ChangePasswordView.as_view()),
    path('captcha/', CaptchaView.as_view())
]
