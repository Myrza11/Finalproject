from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import CaptchaSerializer


'''
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            return Response({'error': 'Confirmation code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUsers.objects.get(confirmation_code=confirmation_code, is_active=False)
        except CustomUsers.DoesNotExist:
            return Response({'error': 'Invalid or expired confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Подтвердите email пользователя
        user.is_active = True
        user.save()

        return Response({'message': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)'''


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Отправка электронной почты с кодом подтверждения
            confirmation_code = user.confirmation_code
            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = 'bapaevmyrza038@gmail.com'  # Укажите ваш отправительский email
            recipient_list = [user.email]

            # Ваш код отправки почты (send_mail)...
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            return Response({'error': 'Confirmation code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUsers.objects.get(confirmation_code=confirmation_code, is_active=False)
        except CustomUsers.DoesNotExist:
            return Response({'error': 'Invalid or expired confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Подтверждение email пользователя
        user.is_active = True
        user.save()

        return Response({'message': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)
    




class CustomUserLoginView(TokenObtainPairView):
    # permission_classes = [AllowAny]
    pass

class CustomUserTokenRefreshView(APIView):
    

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access': access_token,
                             'refresh':token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class CaptchaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CaptchaSerializer(data=request.data)
        if serializer.is_valid():
            # Captcha is valid, continue with your logic
            return Response({'message': 'Captcha is valid'})
        else:
            return Response(serializer.errors, status=400)