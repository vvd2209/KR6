from datetime import datetime
from django.db import models
from config import settings
from mailing.models import Mailing

NULLABLE = {'blank': True, 'null': True}


class Log(models.Model):
    STATUS_CHOICES = (
        ('1', 'Успешно'),
        ('0', 'Неуспешно'),
    )

    time_try = models.DateTimeField(default=datetime.now, verbose_name='дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    client = models.CharField(max_length=150, verbose_name='клиент', **NULLABLE)
    mailing_current = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'Лог: "{self.mailing_current}"'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['-time_try', ]
