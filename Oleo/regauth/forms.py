from captcha.fields import CaptchaField
from rest_framework import serializers

class CaptchaSerializer(serializers.Serializer):
    captcha = CaptchaField()