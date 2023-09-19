from django.db.models.signals import post_save
from django.dispatch import receiver

from exchange_app.models import AccountUSD, AccountRUB, AccountEUR, AccountKGS
from .models import User

@receiver(post_save, sender=User)
def create_user_accounts(sender, instance, created, **kwargs):
    if created:
        AccountUSD.objects.create(user=instance, amount=0)
        AccountRUB.objects.create(user=instance, amount=0)
        AccountEUR.objects.create(user=instance, amount=0)
        AccountKGS.objects.create(user=instance, amount=0)
