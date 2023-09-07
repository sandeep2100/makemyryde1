from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path("", admin_login, name="admin_login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("booking/", bookings, name="booking"),
    path("master_booking/", master_booking, name="master_booking"),
    path("local_booking/", local, name="local_booking"),
    path("roundway_booking/", roundway, name="roundway_booking"),
    path("airport_booking/", airport, name="airport_booking"),
]
