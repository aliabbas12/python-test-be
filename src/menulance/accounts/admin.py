from django.contrib import admin
from accounts.models import UserPreferences


class UserPreferencesAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserPreferences, UserPreferencesAdmin)