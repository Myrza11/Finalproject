from rest_framework import serializers
from .models import CustomUsers
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
    last_name = serializers.CharField(
        required=False,
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.')]
    )
    first_name = serializers.CharField(
        validators=[RegexValidator(regex='^[a-zA-Z]*$', message='Only letters are allowed.')]
    )
    class Meta:
        model = CustomUsers
        fields = '__all__'

    def validate(self, data):
        
        # Проверяем, что пароли совпадают
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")

        return data
    

    def create(self, validated_data):
        confirmation_code = get_random_string(length=20)
        
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            first_name=validated_data['first_name'],
            password=validated_data['password'],
            is_active=False,  # Устанавливаем активность пользователя в False до подтверждения
            confirmation_code=confirmation_code,
        )


                # Отправка электронной почты с кодом подтверждения
        subject = 'Confirmation code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = 'bapaevmyrza038@gmail.com'  # Укажите ваш отправительский email
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return user
    




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True)