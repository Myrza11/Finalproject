

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.TextField()
    recipe = models.TextField()

    def __str__ (self):
        return f"Dish for user {self.user.username}"

    class Meta:
        verbose_name = 'личная еда'
        verbose_name_plural = 'личные блюда'
        ordering = ['user']
