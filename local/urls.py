from django.urls import path
from . import views


urlpatterns = [
    path("local/cab-list/", views.local_cab, name="local_cab"),
    path("local/cab-detail/", views.local_cab_detail, name="local_cab_detail"),
    path("local/cab-booking/", views.local_cab_booking, name="local_cab_booking"),
    path("local/confirm/", views.local_confirm, name="local_confirm"),
]
