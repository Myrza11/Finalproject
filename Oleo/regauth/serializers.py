from rest_framework import serializers
from .models import CustomUsers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUsers
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUsers.objects.create_user(
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            password=validated_data['password'],
        )
        return user