from django import forms

from .models import CarPackage , City , Package , Car


class RouteForm(forms.ModelForm):
    class Meta:
        model = CarPackage
        fields = ["city", "car", "package", "price"]


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name"]


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ["name"]


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["name"]
