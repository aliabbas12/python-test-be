from django.contrib import admin
from contact_us.models import ContactFormEntry


@admin.register(ContactFormEntry)
class ContactFormEntryAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "message")
    search_fields = ("email", "first_name", "last_name")
