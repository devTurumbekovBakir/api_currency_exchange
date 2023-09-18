from django.contrib import admin

from .models import User, StatusUser

admin.site.register(User)
admin.site.register(StatusUser)
