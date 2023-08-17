from django.urls import path
from roundway import views

urlpatterns = [
    path("calculate/", views.calculate, name="calculate"),
    path("roundway/cab-list/", views.round_cab, name="round_cab"),
    path("roundway/cab-detail/", views.round_cab_detail, name="round_cab_detail"),
    path("roundway/cab-booking/", views.round_cab_booking, name="round_cab_booking"),
    path("roundway/confirm/", views.round_confirm, name="round_confirm"),
]
