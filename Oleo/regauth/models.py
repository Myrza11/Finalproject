from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
# Create your models here.
class CustomUsers(AbstractUser):
    first_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.username

    def generate_confirmation_code(self):
        code = get_random_string(length=20)
        return ConfirmationCode.objects.create(user=self, code=code)



class ConfirmationCode(models.Model):
    user = models.ForeignKey('CustomUsers', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.code}"