from account_app.models import User
from exchange_app.models import AccountKGS, AccountUSD, AccountRUB, AccountEUR

user = User.objects.get(is_staff=True)

acc_kgs = AccountKGS.objects.get(user=user)
acc_usd = AccountUSD.objects.get(user=user)
acc_rub = AccountRUB.objects.get(user=user)
acc_eur = AccountEUR.objects.get(user=user)
lists_account = [acc_eur, acc_rub, acc_usd, acc_kgs]


def withdraw_from_account(instance, from_currency, total_sum):
    if instance.code_currency == from_currency.upper():
        instance.amount -= total_sum
        instance.save()


def account_replenishment(instance, to_currency, result):
    if instance.code_currency == to_currency.upper():
        instance.amount += result
        instance.save()


def profit_company(from_currency, discount):
    for account in lists_account:
        if account.code_currency == from_currency.upper():
            account.amount += discount
            account.save()
