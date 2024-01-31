from django.db import models

from client.models import NULLABLE
from config import settings


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(verbose_name='Изображение', **NULLABLE)
    date_of_creation = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'