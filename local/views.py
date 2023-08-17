from django.shortcuts import render, redirect
import math
from .models import City, Package, CarPackage


def local_cab(request):
    selected_city_id = request.session.get("selected_city_id")
    selected_package_id = request.session.get("selected_package_id")
    date = request.session.get("date")
    time = request.session.get("time")

    selected_city = City.objects.get(pk=selected_city_id)
    selected_package = Package.objects.get(pk=selected_package_id)

    selected_car_packages = CarPackage.objects.filter(
        city_id=selected_city_id, package_id=selected_package_id
    )

    return render(
        request,
        "local/cab-list.html",
        {
            "time": time,
            "date": date,
            "selected_car_packages": selected_car_packages,
            "selected_city": selected_city,
            "selected_package": selected_package,
        },
    )


def local_cab_detail(request):
    if request.method == "POST":
        selected_city = request.POST.get("selected_city")
        selected_package = request.POST.get("selected_package")
        car_name = request.POST.get("car_name")
        car_price = request.POST.get("car_price")

        request.session["selected_city"] = selected_city
        request.session["selected_package"] = selected_package
        request.session["car_price"] = car_price
        request.session["car_name"] = car_name

    date = request.session.get("date")
    time = request.session.get("time")

    context = {
        "car_name": car_name,
        "car_price": car_price,
        "selected_city": selected_city,
        "selected_package": selected_package,
        "date": date,
        "time": time,
    }

    return render(request, "local/cab-detail.html", context)


def local_cab_booking(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        pick_up = request.POST.get("mobile")
        remark = request.POST.get("remark")

        date = request.session.get("date")
        time = request.session.get("time")
        car_name = request.session.get("car_name")
        car_price = request.session.get("car_price")
        selected_city = request.session.get("selected_city")
        selected_package = request.session.get("selected_package")

        a = float(car_price)
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        context = {
            "name": name,
            "mobile": mobile,
            "email": email,
            "pick_up": pick_up,
            "remark": remark,
            "date": date,
            "time": time,
            "car_name": car_name,
            "car_price": car_price,
            "selected_package": selected_package,
            "selected_city": selected_city,
            "money": money,
            "money1": money1,
            "money2": money2,
        }
    return render(request, "local/cab-booking.html", context)


def local_confirm(request):
    if request.method == "POST":
        paid = request.POST.get("paid")
    request.session["paid"] = paid

    local_city = request.session.get("local_city")
    booking_id = request.session.get("booking_id")
    name = request.session.get("name")
    money = request.session.get("money")
    paid = request.session.get("paid")
    date = request.session.get("date")
    package = request.session.get("package")
    days = request.session.get("days")
    car_name = request.session.get("car_name")
    pickup_address = request.session.get("pickup_address")

    b = int(paid)
    rem_amount = money - b

    context = {
        "local_city": local_city,
        "booking_id": booking_id,
        "name": name,
        "money": money,
        "paid": paid,
        "rem_amount": rem_amount,
        "date": date,
        "days": days,
        "car_name": car_name,
        "package": package,
        "pickup_address": pickup_address,
    }

    return render(request, "local/confirm.html", context)
