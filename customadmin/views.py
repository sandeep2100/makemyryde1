from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from oneway.models import User, booking
from local.models import local_booking
from airport.models import airport_booking
from roundway.models import roundway_booking
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("/dashboard/")

        if request.method == "POST":
            email = request.method.get("email")
            password = request.method.get("password")
            user_obj = User.objects.filter(email=email)

            if not user_obj.exists():
                messages.info(request, "Account not found")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            user_obj = authenticate(email=email, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect("/dashboard/")

            messages.info(request, "Invalid Password")
            return redirect("/")
        return render(request, "login.html")
    except Exception as e:
        print(e)


def dashboard(request):
    return render(request, "admin/dashboard.html")


def bookings(request):
    objs = booking.objects.all().order_by("-created_at")

    return render(
        request,
        "admin/booking.html",
        {"objs": objs},
    )


def roundway(request):
    roundway = roundway_booking.objects.all().order_by("-created_at")

    return render(
        request,
        "admin/roundway.html",
        {"roundway": roundway},
    )


def local(request):
    local = local_booking.objects.all().order_by("-created_at")

    return render(
        request,
        "admin/local.html",
        {"local": local},
    )


def airport(request):
    airport = airport_booking.objects.all().order_by("-created_at")

    return render(
        request,
        "admin/airport.html",
        {"airport": airport},
    )


def master_booking(request):
    all_bookings = []

    objs = booking.objects.all().order_by("-created_at")
    local = local_booking.objects.all().order_by("-created_at")
    roundway = roundway_booking.objects.all().order_by("-created_at")
    airport = airport_booking.objects.all().order_by("-created_at")

    all_bookings.extend(objs)
    all_bookings.extend(local)
    all_bookings.extend(roundway)
    all_bookings.extend(airport)

    all_bookings.sort(key=lambda x: x.created_at, reverse=True)

    return render(
        request,
        "admin/master_booking.html",
        {"all_bookings": all_bookings},
    )
