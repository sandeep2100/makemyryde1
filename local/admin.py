from django.contrib import admin
from .models import *


class CarPackageInline(admin.TabularInline):
    model = CarPackage
    extra = 1
    readonly_fields = ["car", "package"]  # Make car and package fields read-only
    fields = ["car", "package", "price"]


class CityAdmin(admin.ModelAdmin):
    inlines = [CarPackageInline]

    def display_car_packages(self, obj):
        car_packages = CarPackage.objects.filter(city=obj)
        return ", ".join(
            [f"{cp.package.name} - {cp.price} - {cp.car.name}" for cp in car_packages]
        )

    display_car_packages.short_description = "Car Packages"


class CarAdmin(admin.ModelAdmin):
    pass


class PackageAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(CarPackage)
