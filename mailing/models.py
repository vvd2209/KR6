from django.db import models

from client.models import Client
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Mailing(models.Model):
    PERIODICITY_CHOICES = (
        ('1', 'Раз в день'),
        ('2', 'Раз в неделю',),
        ('3', 'Раз в месяц',),
    )

    STATUS_CHOICES = (
        ('1', 'Создана'),
        ('2', 'Запущена',),
        ('3', 'Завершена',),
    )

    start_time = models.DateTimeField(verbose_name='время начала рассылки', **NULLABLE)
    end_time = models.DateTimeField(verbose_name='время окончания рассылки', **NULLABLE)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, verbose_name='периодичность',
                                   **NULLABLE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=1, verbose_name='статус рассылки')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты рассылки', **NULLABLE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='рассылка', **NULLABLE)

    def __str__(self):
        return f'time: {self.start_time} - {self.end_time}, periodicity: {self.periodicity}, status: {self.status}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылки'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
