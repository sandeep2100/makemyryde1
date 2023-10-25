from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path("", admin_login, name="admin_login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("booking/", bookings, name="booking"),
    path("master_booking/", master_booking, name="master_booking"),
    path("local_booking/", local, name="local_booking"),
    path("roundway_booking/", roundway, name="roundway_booking"),
    path("airport_booking/", airport, name="airport_booking"),
    path("fix_routes/", fix_routes, name="fix_routes"),
    path("popular_routes/", popular_routes, name="popular_routes"),
    path("inquiry/", inquiry, name="inquiry"),
    path("number/", dynamic_number, name="number"),
    path("update_number/<int:number_id>/", update_number, name="update_number"),
    path("coupon_list/", coupon_list, name="coupon_list"),
    path("update/<int:coupon_id>/", coupon_update, name="coupon_update"),
    path("add/", coupon_add, name="coupon_add"),
    path("cab-fare-oneway/", cab_fare, name="cab_fare_oneway"),
    path("cab-fare-roundway/", cab_fare_roundway, name="cab_fare_roundway"),
    path("dynamic-route/", dynamic_page, name="dynamic_route"),
    path("dynamic-roundway/", dynamic_roundway, name="dynamic_roundway"),
    path("dynamic-local/", dynamic_local, name="dynamic_local"),
    path("routes/", route_list, name="route_list"),
    path("add_city/", add_city, name="add_city"),
    path("add_package/", add_package, name="add_package"),
    path("add_car/", add_car, name="add_car"),
    path("routes/create/", create_route, name="create_route"),
    path("routes/<int:route_id>/update/", update_route, name="update_route"),
    path("routes/<int:route_id>/delete/", delete_route, name="delete_route"),
    path("edit-social/", edit_social, name="edit_social"),
    path("admin/logo-settings/", logo_settings_view, name="logo_settings"),
    path("email/", edit_emails, name="email"),
    path("edit_fix_route/<int:route_id>/", edit_fix_route, name="edit_fix_route"),
    path("delete_fix_route/<int:route_id>/", delete_fix_route, name="delete_fix_route"),
    path("onewayprice/", OnewayCab, name="onewayprice"),
    path("airport_base/", airport_base, name="airport_base"),
    path("cab-fare-airport/", cab_fare_airport, name="cab_fare_airport"),
    path(
        "edit_oneway/<int:route_id>/", edit_dynamic_oneway, name="edit_dynamic_oneway"
    ),
    path(
        "edit_roundway/<int:route_id>/",
        edit_dynamic_roundway,
        name="edit_dynamic_roundway",
    ),
    path(
        "delete_roundway/<int:route_id>/",
        delete_dynamic_roundway,
        name="delete_dynamic_roundway",
    ),
    path(
        "delete_oneway/<int:route_id>/",
        delete_dynamic_oneway,
        name="delete_dynamic_oneway",
    ),
    path("edit_local/<int:route_id>/", edit_dynamic_local, name="edit_dynamic_local"),
    path(
        "delete_local/<int:route_id>/",
        delete_dynamic_local,
        name="delete_dynamic_local",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
