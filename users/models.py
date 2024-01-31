from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=250, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=250, verbose_name='фамилия', **NULLABLE)
    verification_code = models.CharField(max_length=256, verbose_name='код для проверки', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="пользователь активен")

    # переопределение поля юзернейма
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
