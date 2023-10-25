from django.db import models


class Social(models.Model):
    facebook_admin = models.CharField(max_length=200)
    instagram_admin = models.CharField(max_length=200)
    twitter_admin = models.CharField(max_length=200)


class LogoSettings(models.Model):
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)


class Email(models.Model):
    booking_email = models.EmailField()
    info_email = models.EmailField()
