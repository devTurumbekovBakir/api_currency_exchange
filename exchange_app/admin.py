from django.contrib import admin

from .models import AccountUsd, AccountEur, AccountRub, AccountSom

admin.site.register(AccountUsd)
admin.site.register(AccountEur)
admin.site.register(AccountRub)
admin.site.register(AccountSom)
