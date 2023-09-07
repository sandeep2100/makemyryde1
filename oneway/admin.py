from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'mobile', 'email', 'is_staff')
    search_fields = ('username', 'mobile', 'email')




admin.site.register(User, CustomUserAdmin)
admin.site.register(booking)
admin.site.register(Cars)


