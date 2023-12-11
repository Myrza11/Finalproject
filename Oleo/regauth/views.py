from django.conf import settings
from django.shortcuts import render

# Create your views here.
from .models import ConfirmationCode
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .forms import CaptchaSerializer
from rest_framework import generics, status
from django.contrib.auth.views import LogoutView
from rest_framework.decorators import api_view, permission_classes

# //    РЕГИСТРАЦИЯ      \\

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
    
    
    # //    ПРОВЕРКА ПОДТВЕРДИТЕЛЬНОГО КОДА      \\
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
        






# //    ИЗМЕНЕНИЕ ПАРОЛЯ И USERNAME     \\

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            # Проверка старого пароля
            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Установка нового пароля
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_username = serializer.data.get("new_username")

            user.username = new_username
            user.save()

            return Response({"detail": "Username changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# //    СБРОС ПАРОЛЯ      \\

class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    queryset = CustomUsers.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Получаем QuerySet всех пользователей с заданным адресом электронной почты
        users = CustomUsers.objects.filter(email=email)

        if not users.exists():
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Генерация кода подтверждения
        confirmation_code = get_random_string(length=20)

        # Создание объекта ConfirmationCode для пользователя
        user = users[0]  # Предполагаем, что email уникален
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        # Отправка кода на email пользователя
        subject = 'Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Confirmation code sent successfully.'})


class ResetPasswordView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            confirmation_code = serializer.validated_data.get("confirmation_code")
            new_password = serializer.validated_data.get("new_password")
            
            try:
                confirmation = ConfirmationCode.objects.get(user__email=email, code=confirmation_code)
            except ConfirmationCode.DoesNotExist:
                return Response({"detail": "Invalid or expired confirmation code."}, status=status.HTTP_400_BAD_REQUEST)

            user = confirmation.user
            user.set_password(new_password)
            user.save()

            confirmation.delete()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# //    КАПЧА      \\

class CaptchaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CaptchaSerializer(data=request.data)
        if serializer.is_valid():
            # Captcha is valid, continue with your logic
            return Response({'message': 'Captcha is valid'})
        else:
            return Response(serializer.errors, status=400)