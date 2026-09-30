"""Admin configuration for the LegacyModel."""


from django.contrib import admin

from .models import LegacyModel


class LegacyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'legacy_code', 'created_at')

admin.site.register(LegacyModel, LegacyModelAdmin)
