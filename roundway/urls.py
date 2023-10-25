from django.urls import path
from roundway import views

urlpatterns = [
    path("calculate/", views.calculate, name="calculate"),
    path("roundway/cab-list/", views.round_cab, name="round_cab"),
    path("roundway/cab-detail/", views.round_cab_detail, name="round_cab_detail"),
    path("roundway/cab-booking/", views.round_cab_booking, name="round_cab_booking"),
    path(
        "roundway/confirm/<str:booking_id>/", views.round_confirm, name="round_confirm"
    ),
    path(
        "roundway/generate_invoice/<int:booking_id>/",
        views.generate_invoice_html,
        name="generate_invoice_pdf_rw",
    ),
    path(
        "roundway/send_invoice/<str:booking_id>/",
        views.send_invoice_email,
        name="send_invoice_roundway",
    ),
]
