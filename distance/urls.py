from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from oneway import views


urlpatterns = [
    path("dj-admin/", admin.site.urls),
    path("", views.INDEX, name="index"),
    path("oneway/cab-list/", views.CAB, name="cab_list"),
    path("oneway/cab-detail/", views.CAB_DETAIL, name="cab-detail"),
    path("oneway/cab-booking/", views.CAB_BOOKING, name="cab-booking"),
    path("oneway/confirm/<str:booking_id>/", views.CONFIRM, name="confirm"),
    path("validate-coupon/", views.validate_coupon, name="validate_coupon"),
    path("calculate-fare/", views.calculate_fare, name="calculate-fare"),
    # path('register/', views.REGISTER, name='register'),
    path("login/", views.LOGIN, name="login"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("for-password/", views.PASSWORD, name="password"),
    path("profile/", views.PROFILE, name="profile"),
    path("privacy-policy/", views.PRIVACY, name="privacy"),
    path("terms-conditions/", views.terms, name="terms"),
    path("refund/", views.refund, name="refund"),
    path("demo/", views.DEMO, name="demo"),
    path("error/", views.ERROR, name="error"),
    path("About-us/", views.aboutus, name="aboutus"),
    path("Contact-us/", views.contactus, name="contactus"),
    path("header/", views.header, name="header"),
    path("oneway/invoice/", views.INVOICE, name="invoice"),
    # Oneway Dynamic
    path("route/<slug:custom_url>/", views.oneway_dynamic, name="oneway_dynamic"),
    path("routes/", views.oneway_route_list, name="oneway_route_list"),
    path(
        "round-way-cabs/",
        views.roundway_city_list,
        name="roundway-city-list",
    ),
    path(
        "round-way-cabs/<str:city>/",
        views.roundway_city_route,
        name="roundway_city_routes",
    ),
    path("round-way/<slug:custom_url>/", views.route_detail, name="route_detail"),
    # Local Dynamic
    path("all_cities/", views.all_cities, name="all_cities"),
    path(
        "local-cab/<str:city_name>/<str:custom_url>/",
        views.city_detail,
        name="city_detail",
    ),
    # Airport Dynamic
    path("airport-cabs/", views.dynamic_airport, name="dynamic_airport"),
    path(
        "generate_invoice/<int:booking_id>/",
        views.generate_invoice_html,
        name="generate_invoice_pdf",
    ),
    path(
        "send_invoice/<str:booking_id>/",
        views.send_invoice_email,
        name="send_invoice_oneway",
    ),
    path("popular-routes/", views.popular, name="popular"),
    path("admin/", include("customadmin.urls")),
    path("", include("oneway.urls")),
    path("", include("roundway.urls")),
    path("", include("local.urls")),
    path("", include("airport.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
