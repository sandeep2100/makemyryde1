from django.urls import path

from . import views

urlpatterns = [
    path("local/cab-list/", views.local_cab, name="local_cab"),
    path("local/cab-detail/", views.local_cab_detail, name="local_cab_detail"),
    path("local/cab-booking/", views.local_cab_booking, name="local_cab_booking"),
    path("local/confirm/<str:booking_id>/", views.local_confirm, name="local_confirm"),
    path(
        "local/generate_invoice/<int:booking_id>/",
        views.generate_invoice_html,
        name="generate_invoice_pdf_lc",
    ),
    path(
        "local/send_invoice/<str:booking_id>/",
        views.send_invoice_email,
        name="send_invoice_email_lc",
    ),
    path("local/invoice/", views.invoice),
]
