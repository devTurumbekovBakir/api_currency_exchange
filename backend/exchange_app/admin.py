from django.contrib import admin

from .models import AccountUSD, AccountEUR, AccountRUB, AccountKGS, Transaction

admin.site.register(AccountUSD)
admin.site.register(AccountEUR)
admin.site.register(AccountRUB)
admin.site.register(AccountKGS)
admin.site.register(Transaction)
