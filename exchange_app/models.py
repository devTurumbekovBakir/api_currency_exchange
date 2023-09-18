from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAbstract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'
        abstract = True

    def __str__(self):
        return f'{self.user.username} - {self.amount}'


class AccountUsd(AccountAbstract):
    ...


class AccountRub(AccountAbstract):
    ...


class AccountEur(AccountAbstract):
    ...


class AccountSom(AccountAbstract):
    ...


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form_currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    to_currency = models.CharField(max_length=3)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
