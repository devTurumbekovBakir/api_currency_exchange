def withdraw_from_account(instance, from_currency, total_sum):
    if instance.code_currency == from_currency.upper():
        instance.amount -= total_sum
        instance.save()


def account_replenishment(instance, to_currency, result):
    if instance.code_currency == to_currency.upper():
        instance.amount += result
        instance.save()