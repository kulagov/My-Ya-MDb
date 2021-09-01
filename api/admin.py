from django.contrib import admin

from .models import UserConfirmationCode


class UserConfAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'confirmation_code')


admin.site.register(UserConfirmationCode, UserConfAdmin)
