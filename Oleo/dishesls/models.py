from django.db import models


# Create your models here.

class Category(models.Model):
    types = models.CharField(max_length=50)

    def __str__ (self):
        return self.types

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        ordering = ['types']





class Food(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(verbose_name='Фотки', upload_to='photos/%Y/%m/%d')
    recept = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category',related_name='category', default=False)

    def __str__ (self):
        return self.name

    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еды'
        ordering = ['name']

class Coment(models.Model):
    title = models.TextField()

    def __str__ (self):
        return self.name

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['name']