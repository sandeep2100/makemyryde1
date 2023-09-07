from django.urls import path
from airport import views

urlpatterns = [
    path("airport/cab-list/", views.airport_cab, name="airport_cab"),
    path("airport/cab-detail/", views.airport_cab_detail, name="airport_cab_detail"),
    path("airport/cab-booking/", views.airport_cab_booking, name="airport_cab_booking"),
    path("airport/confirm/", views.airport_confirm, name="airport_confirm"),
    # path("airport-fare/", views.airport_fare, name="airport-fare"),
]
