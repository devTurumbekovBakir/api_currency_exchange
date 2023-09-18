from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    passport_id = models.CharField(max_length=9)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
