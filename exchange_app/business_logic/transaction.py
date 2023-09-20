from rest_framework.exceptions import ValidationError

from exchange_app.models import AccountKGS, AccountUSD, AccountRUB, AccountEUR


def withdraw_from_account(instance, from_currency, amount):
    if instance.amount < amount and instance.code_currency == from_currency.upper():
        raise ValidationError('У вас недостаточна средств на счету')
    elif instance.code_currency == from_currency.upper():
        instance.amount -= amount
        instance.save()


def account_replenishment(instance, to_currency, result, user_discount):
    discount = result * user_discount / 100
    if instance.code_currency == to_currency.upper():
        profit_company(to_currency, discount)
        instance.amount += result - discount
        instance.save()


def profit_company(code_currency, discount):
    lists_account = [
        AccountKGS.objects.get(user__username='admin'),
        AccountUSD.objects.get(user__username='admin'),
        AccountRUB.objects.get(user__username='admin'),
        AccountEUR.objects.get(user__username='admin')]
    for account in lists_account:
        if account.code_currency == code_currency.upper():
            account.amount += discount
            account.save()
