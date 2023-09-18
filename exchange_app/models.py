from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAbstract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user.username} - {self.amount}'


class AccountUsd(AccountAbstract):
    class Meta:
        verbose_name = 'Счет Доллар'
        verbose_name_plural = 'Счета Доллары'


class AccountRub(AccountAbstract):
    class Meta:
        verbose_name = 'Счет Рубль'
        verbose_name_plural = 'Счета Рубли'


class AccountEur(AccountAbstract):
    class Meta:
        verbose_name = 'Счет Евро'
        verbose_name_plural = 'Счета Евро'


class AccountSom(AccountAbstract):
    class Meta:
        verbose_name = 'Счет Сом'
        verbose_name_plural = 'Счета Сомы'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=3)
    amount = models.FloatField()
    to_currency = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
