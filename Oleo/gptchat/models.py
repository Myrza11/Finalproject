

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.TextField()

    def __str__ (self):
        return self.user

    class Meta:
        verbose_name = 'личная еда'
        verbose_name_plural = 'личные блюда'
        ordering = ['user']
