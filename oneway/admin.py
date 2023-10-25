from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import activate

from .models import *


# Register your models here.


class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        activate("Asia/Kolkata")  # Set the timezone to IST
        return context


admin.site = CustomAdminSite()


@admin.register(OneWayRoute)
class OneWayRouteAdmin(admin.ModelAdmin):
    list_display = (
        "source_city",
        "destination_city",
        "hatchback_price",
        "sedan_price",
        "suv_price",
    )


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "mobile", "email", "is_staff")
    search_fields = ("username", "mobile", "email")


admin.site.register(OnewayCityFix)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cars)
admin.site.register(Routes)
admin.site.register(booking)
# admin.site.register(Confirm_Payment)
admin.site.register(PerKmPrices)
admin.site.register(OnewayPrice)
