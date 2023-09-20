from django.contrib import admin

from .models import User, StatusUser, ConfirmationCode

admin.site.register(User)
admin.site.register(StatusUser)
admin.site.register(ConfirmationCode)
