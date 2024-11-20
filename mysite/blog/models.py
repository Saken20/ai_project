# blog/models.py
from django.db import models

class Contacts(models.Model):
    name = models.CharField(max_length=150, verbose_name='имя')
    number = models.CharField(max_length=18, verbose_name='номер')
    email = models.EmailField(max_length=254, verbose_name='email')
    message = models.TextField(verbose_name='Сообщение')

    class Meta:
        db_table = 'contact'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name
