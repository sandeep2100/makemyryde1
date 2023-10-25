from django.contrib import admin

from .models import *

admin.site.register(Email)
admin.site.register(Social)


@admin.register(LogoSettings)
class LogoSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "logo",
    )
