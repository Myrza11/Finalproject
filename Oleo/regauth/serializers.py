from rest_framework import serializers
from .models import CustomUsers
from django.core.validators import RegexValidator


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
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
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            first_name=validated_data['first_name'],
            password=validated_data['password'],
        )
        return user