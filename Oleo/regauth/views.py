from django.conf import settings
from django.shortcuts import render
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

# Отправляем код пользователю, 
# далльше проверяем код который мы создали с кодом который написал пользователь если они совпадают то активируем пользователя
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            confirmation_code = user.confirmation_code
            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = 'bapaevmyrza038@gmail.com'  
            recipient_list = [user.email]

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
        

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

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


class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer
    queryset = CustomUsers.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        users = CustomUsers.objects.filter(email=email)

        if not users.exists():
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        confirmation_code = get_random_string(length=20)

        user = users[0]  
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        subject = 'Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Confirmation code sent successfully.'})


class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer
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
                return Response({"detail": "Invalid or expired confirmation code or wrong email."}, status=status.HTTP_400_BAD_REQUEST)

            user = confirmation.user
            user.set_password(new_password)
            user.save()

            confirmation.delete()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaptchaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CaptchaSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Captcha is valid'})
        else:
            return Response(serializer.errors, status=400)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUsers.objects.all()


class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUsers.objects.all()

    def partial_update(self, request, *args, **kwargs):
        allowed_fields = ['avatar']
        data = {k: v for k, v in request.data.items() if k in allowed_fields}

        serializer = self.get_serializer(self.get_object(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)