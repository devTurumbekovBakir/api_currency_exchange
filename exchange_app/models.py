from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAbstract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user.username} - {self.code_currency}'


class AccountUSD(AccountAbstract):
    code_currency = models.CharField(max_length=3, default='USD')

    class Meta:
        verbose_name = 'Счет USD'
        verbose_name_plural = 'Счета USD'


class AccountRUB(AccountAbstract):
    code_currency = models.CharField(max_length=3, default='RUB')

    class Meta:
        verbose_name = 'Счет RUB'
        verbose_name_plural = 'Счета RUB'


class AccountEUR(AccountAbstract):
    code_currency = models.CharField(max_length=3, default='EUR')

    class Meta:
        verbose_name = 'Счет EUR'
        verbose_name_plural = 'Счета EUR'


class AccountKGS(AccountAbstract):
    code_currency = models.CharField(max_length=3, default='KGS')

    class Meta:
        verbose_name = 'Счет KGS'
        verbose_name_plural = 'Счета KGS'


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
