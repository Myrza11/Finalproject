from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUsers(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.username
