from django.urls import path
from airport import views

urlpatterns = [
    path("airport/cab-list/", views.airport_cab, name="airport_cab"),
    path("airport/cab-detail/", views.airport_cab_detail, name="airport_cab_detail"),
    path("airport/cab-booking/", views.airport_cab_booking, name="airport_cab_booking"),
    path(
        "airport/confirm/<str:booking_id>/",
        views.airport_confirm,
        name="airport_confirm",
    ),
    # path("airport-fare/", views.airport_fare, name="airport-fare"),
    path(
        "airport/generate_invoice/<int:booking_id>/",
        views.generate_invoice_html,
        name="generate_invoice_pdf",
    ),
    path(
        "airport/send_invoice/<str:booking_id>/",
        views.send_invoice_email,
        name="send_invoice_email",
    ),
]
