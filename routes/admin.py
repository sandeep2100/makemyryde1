from django.contrib import admin
from .models import *


class RouteInline(admin.TabularInline):
    model = Route
    extra = 0  # This removes the extra empty forms for routes


class CityAdmin(admin.ModelAdmin):
    list_display = ("city",)
    inlines = [RouteInline]


admin.site.register(City1, CityAdmin)
admin.site.register(Local_City)
admin.site.register(Oneway_routes)
admin.site.register(Roundway_routes)
