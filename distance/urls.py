from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myapp import views


urlpatterns = [
    path("dj-admin/", admin.site.urls),
    path("", views.INDEX, name="index"),
    path("oneway/cab-list/", views.CAB, name="cab_list"),
    path("oneway/cab-detail/", views.CAB_DETAIL, name="cab-detail"),
    path("oneway/cab-booking/", views.CAB_BOOKING, name="cab-booking"),
    path("oneway/confirm/", views.CONFIRM, name="confirm"),
    path("calculate-fare/", views.calculate_fare, name="calculate-fare"),
    # path('register/', views.REGISTER, name='register'),
    path("login/", views.LOGIN, name="login"),
    path("logout_view/", views.logout_view, name="logout_view"),
    path("for-password/", views.PASSWORD, name="password"),
    path("profile/", views.PROFILE, name="profile"),
    path("privacy/", views.PRIVACY, name="privacy"),
    path("demo/", views.DEMO, name="demo"),
    path("admin/", include("customadmin.urls")),
    path("", include("myapp.urls")),
    path("", include("roundway.urls")),
    path("", include("local.urls")),
    path("", include("airport.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
