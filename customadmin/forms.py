from django import forms

from .models import *


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["booking_email", "info_email"]


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = ["facebook_admin", "instagram_admin", "twitter_admin"]
