from django.db import models


class City1(models.Model):
    city = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.city


class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    custom_url = models.SlugField(unique=True)
    city = models.ForeignKey(City1, on_delete=models.CASCADE)

    def __str__(self):
        return self.custom_url


class Local_City(models.Model):
    city_name = models.CharField(max_length=100)
    local_city = models.CharField(max_length=200)
    custom_url = models.SlugField(unique=True)

    def __str__(self):
        return self.city_name


class Oneway_routes(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    custom_url = models.SlugField(unique=True)

    def __str__(self):
        return self.custom_url


class Roundway_routes(models.Model):
    roundway_city = models.CharField(max_length=100, default="")
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    custom_url = models.SlugField(unique=True)

    def __str__(self):
        return self.custom_url
