from django.db import models
from django.contrib.auth.models import AbstractUser


class StatusUser(models.Model):
    number = models.PositiveIntegerField(help_text="Идентификатор статуса")
    description = models.CharField(max_length=50)
    discount = models.FloatField(help_text="Коммиссия")

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f'{self.number} - {self.discount} - {self.description}'


class User(AbstractUser):
    passport_id = models.CharField(max_length=9, null=True, blank=True,
                                   help_text='Введите ID паспорта, если вы гражданин КР')
    status = models.ForeignKey(StatusUser, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'


class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Код подтверждения'

    def __str__(self):
        return f'{self.code} - {self.user.username}'
