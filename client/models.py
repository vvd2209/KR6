from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    email = models.EmailField(max_length=100, verbose_name='контактный email')
    comment = models.TextField(max_length=500, verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
