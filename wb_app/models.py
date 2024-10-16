from django.db import models

class Product(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Название бренда')
    name = models.CharField(max_length=255, verbose_name='Название товара')
    price = models.CharField(max_length=255,verbose_name='Цена товара')
    color = models.CharField(max_length=50, verbose_name='Цвет товара')
    rating = models.FloatField(verbose_name='Рейтинг товара')
    number_of_ratings = models.IntegerField(verbose_name='Количество оценок')
    options = models.JSONField(verbose_name='Опции')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
