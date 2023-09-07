from django.shortcuts import render, redirect, HttpResponse
import json
import math
from .models import *
from decimal import Decimal
from django.http import JsonResponse


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

    gst_rate = Decimal("0.05")

    fare_summaries = []
    for car_package in selected_car_packages:
        total_price = car_package.price
        estimated_amount = total_price * (1 - gst_rate)
        gst_amount = total_price * gst_rate

        estimated_amount = math.ceil(estimated_amount)
        gst_amount = math.ceil(gst_amount)
        total_price = math.ceil(total_price)

        fare_summary = {
            "car_package": car_package,
            "estimated_amount": estimated_amount,
            "gst_amount": gst_amount,
            "actual_price": total_price,
        }
        fare_summaries.append(fare_summary)

    return render(
        request,
        "local/cab-list.html",
        {
            "time": time,
            "date": date,
            "selected_car_packages": selected_car_packages,
            "selected_city": selected_city,
            "selected_package": selected_package,
            "fare_summaries": fare_summaries,
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
        mobile_b = request.POST.get("mobile")
        email = request.POST.get("email")
        pick_up = request.POST.get("pick_up")
        booking_id = request.POST.get("booking_id")
        remark = request.POST.get("remark")
        booking_type = request.POST.get("booking_type")
        gst_company = request.POST.get("gst_company")
        gst_number = request.POST.get("gst_number")
        alternative_number = request.POST.get("alternative_number")
        amount = request.POST.get("amount")
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")

        date = request.session.get("date")
        time = request.session.get("time")
        car_name = request.session.get("car_name")
        car_price = request.session.get("car_price")
        selected_city = request.session.get("selected_city")
        selected_package = request.session.get("selected_package")

        en = local_booking(
            name=name,
            email=email,
            mobile_b=mobile_b,
            pick_up=pick_up,
            selected_city=selected_city,
            booking_id=booking_id,
            selected_package=selected_package,
            date=date,
            car_price=car_price,
            time=time,
            remark=remark,
            gst_number=gst_number,
            gst_company=gst_company,
            amount=amount,
            booking_type=booking_type,
            alternative_number=alternative_number,
        )
        en.save()
        booking_id = en.booking_id

        a = float(amount)
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        context = {
            "name": name,
            "mobile_b": mobile_b,
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
            "booking_type": booking_type,
            "booking_id": booking_id,
            "amount": amount,
            "coupon_price": coupon_price,
            "coupon_code": coupon_code,
        }

        request.session["name"] = name
        request.session["mobile"] = mobile_b
        request.session["email"] = email
        request.session["pick_up"] = pick_up
        request.session["booking_id"] = booking_id
        request.session["remark"] = remark
        request.session["booking_type"] = booking_type
        request.session["money"] = money
        request.session["coupon_price"] = coupon_price
        request.session["coupon_code"] = coupon_code

        return render(request, "local/cab-booking.html", context)


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def local_confirm(request):
    name = request.session.get("name")
    email = request.session.get("email")
    mobile = request.session.get("mobile")
    booking_id = request.session.get("booking_id")
    date = request.session.get("date")
    time = request.session.get("time")
    car_name = request.session.get("car_name")
    car_price = request.session.get("car_price")
    selected_city = request.session.get("selected_city")
    selected_package = request.session.get("selected_package")
    money = request.session.get("money")
    pick_up = request.session.get("pick_up")
    coupon_price = request.session.get("coupon_price")
    coupon_code = request.session.get("coupon_code")

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = int(total) - b

        context = {
            "selected_city": selected_city,
            "booking_id": booking_id,
            "name": name,
            "email": email,
            "money": money,
            "mobile": mobile,
            "time": time,
            "paid": paid,
            "date": date,
            "car_price": car_price,
            "selected_package": selected_package,
            "car_name": car_name,
            "pick_up": pick_up,
            "rem_amount": rem_amount,
            "total": total,
            "coupon_price": coupon_price,
            "coupon_code": coupon_code,
        }
        return render(request, "local/confirm.html", context)
