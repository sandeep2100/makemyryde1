import math
from datetime import datetime

import googlemaps
import requests
from contact.models import Contact , Number
from coupon.models import Coupon
from customadmin.models import Social , Email
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse , JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render , get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from local.models import City , Package , CarPackage
from routes.models import Route , Local_City , Oneway_routes , Roundway_routes

from .models import *


@csrf_exempt
def validate_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")

        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.expiration_date >= timezone.now().date():
                response_data = {
                    "valid": True,
                    "discount_amount": coupon.discount_value,
                }
            else:
                response_data = {"valid": False, "message": "Coupon is expired."}
        except Coupon.DoesNotExist:
            response_data = {"valid": False, "message": "Invalid Coupon Code."}

        return JsonResponse(response_data)


def header(request):
    number = Number.objects.all()

    context = {"number": number}
    return render(request, "include/header.html", context)


def calculate_distance(source, destination):
    # Initialize Google Maps API client
    gmaps = googlemaps.Client(key="AIzaSyAX0OjsvGZFaLvdaYyOvaWvRmSpnEqVNIo")

    # Make API request to calculate distance
    response = gmaps.distance_matrix(source, destination, mode="driving")

    # Extract distance value from response
    distance = response["rows"][0]["elements"][0]["distance"]["value"]

    # Convert distance from meters to kilometers
    distance_km = distance / 1000

    return distance_km


def dynamic_airport(request):
    number = Number.objects.all()
    return render(request, "routes/airport_dynamic.html", {"number": number})


def all_cities(request):
    number = Number.objects.all()
    cities1 = Local_City.objects.all()
    return render(
        request, "routes/all_cities.html", {"cities1": cities1, "number": number}
    )


def city_detail(request, custom_url, city_name):
    number = Number.objects.all()
    city = get_object_or_404(Local_City, custom_url=custom_url, city_name=city_name)
    return render(
        request,
        "routes/city_detail.html",
        {"city": city, "city_name": city_name, "number": number},
    )


def INDEX(request):
    cities = City.objects.all()
    packages = Package.objects.all()
    number = Number.objects.all()

    if request.method == "POST":
        selected_city_id = request.POST.get("city")
        selected_package_id = request.POST.get("package")
        date = request.POST.get("date")
        time = request.POST.get("time")

        # selected_city = City.objects.get(pk=selected_city_id)
        # selected_package = Package.objects.get(pk=selected_package_id)

        selected_car_packages = CarPackage.objects.filter(
            city_id=selected_city_id, package_id=selected_package_id
        )
        request.session["selected_city_id"] = selected_city_id
        request.session["selected_package_id"] = selected_package_id
        request.session["date"] = date
        request.session["time"] = time

        return redirect(
            reverse("local_cab"),
            {
                # "selected_city": selected_city,
                # "selected_package": selected_package,
                "selected_car_packages": selected_car_packages,
                "date": date,
                "time": time,
            },
        )

    return render(
        request,
        "index.html",
        {"cities": cities, "packages": packages, "number": number},
    )


# def REGISTER(request):

# if request.method == 'POST':
#   username = request.POST.get('username')
#   mobile = request.POST.get('mobile')
#   email = request.POST.get('email')
#   password = request.POST.get('password')


#  if User.objects.filter(mobile=mobile).exists():
#     messages.error(request, 'mobile is already exists')
#     return redirect('login')

# if User.objects.filter(email=email).exists():
#      messages.error(request, 'email id is already exists')
#     return redirect('login')

#  user = User(
#      mobile=mobile,
#      email=email,
#     username=username,
# )
# user.set_password(password)
# user.save()
# return redirect('login')
# return render(request, 'register.html')


def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Email or Password are Invalid !")
            return redirect("login")

    return render(request, "login.html")


def calculate_fare(request):
    per_km_prices = PerKmPrices.objects.first()
    oneway_prices = OnewayPrice.objects.first()
    if request.method == "POST":
        booking_type = request.POST.get("booking_type")
        source = request.POST.get("source")  # Get the source as a string, not a list
        destination = request.POST.get(
            "destination"
        )  # Get the destination as a string, not a list
        date = request.POST.get("date")
        time1 = request.POST.get("time")
        # re_date = request.POST.getlist('re_date')
        # re_time = request.POST.getlist('re_time')

        # time_obj = datetime.strptime(time[0], "%H:%M")
        # formatted_time = time_obj.strftime("%I:%M %p")

        time24 = time1
        time_obj = datetime.strptime(time24, "%H:%M")
        time = time_obj.strftime("%I:%M %p")

        distance = calculate_distance(source, destination)
        toll_tax = distance

    if per_km_prices:
        per_km_price1 = float(per_km_prices.price1)
        per_km_price2 = float(per_km_prices.price2)
        per_km_price3 = float(per_km_prices.price3)
        per_km_price4 = float(per_km_prices.price4)

        if distance < 50:
            per_km_price1 = float(oneway_prices.price1)
            per_km_price2 = float(oneway_prices.price2)
            per_km_price3 = float(oneway_prices.price3)
            per_km_price4 = float(oneway_prices.price4)
        elif distance < 75:
            per_km_price1 = float(oneway_prices.price5)
            per_km_price2 = float(oneway_prices.price6)
            per_km_price3 = float(oneway_prices.price7)
            per_km_price4 = float(oneway_prices.price8)

        base_fare1 = distance * per_km_price1
        base_fare2 = distance * per_km_price2
        base_fare3 = distance * per_km_price3
        base_fare4 = distance * per_km_price4

        try:
            route = OneWayRoute.objects.get(
                source_city=source, destination_city=destination
            )
            base_fare1 = route.hatchback_price
            base_fare2 = route.sedan_price
            base_fare3 = route.suv_price
        except OneWayRoute.DoesNotExist:
            # Handle the case when no matching route is found
            hatchback_price = base_fare1
            sedan_price = base_fare2
            suv_price = base_fare3

        # if any(place in source for place in places) and any(
        #     place in destination for place in places
        ## ):
        #     base_fare1 = base_fare1
        #     base_fare2 = base_fare2
        #     base_fare3 = base_fare3
        #     base_fare4 = base_fare4  # Base fare when both source and destination are in the array
        # elif any(place in source for place in places) or any(
        #    place in destination for place in places
        ##):
        #     base_fare1 += 1500
        #     base_fare2 += 1500
        #     base_fare3 += 1500
        #     base_fare4 += 1500  # Base fare + additional fare when either source or destination is in the array
        # else:
        #   base_fare1 += 3000
        #    base_fare2 += 3000
        #    base_fare3 += 3000
        #    base_fare4 += 3000  # Base fare + additional fare when neither source nor destination is in the array

        gst1 = base_fare1 * 0.05  # Add 5% GST amount
        gst2 = base_fare2 * 0.05
        gst3 = base_fare3 * 0.05
        gst4 = base_fare4 * 0.05

        total_fare1 = base_fare1 + gst1
        total_fare2 = base_fare2 + gst2
        total_fare3 = base_fare3 + gst3
        total_fare4 = base_fare4 + gst4  # Add 5% GST amount

        fare1 = total_fare1 * 0.15
        fare2 = total_fare2 * 0.15
        fare3 = total_fare3 * 0.15
        fare4 = total_fare4 * 0.15

        dis_fare1 = fare1 + total_fare1
        dis_fare2 = fare2 + total_fare2
        dis_fare3 = fare3 + total_fare3
        dis_fare4 = fare4 + total_fare4

        distance = round(distance)

        total_fare1 = math.ceil(total_fare1)
        total_fare2 = math.ceil(total_fare2)
        total_fare3 = math.ceil(total_fare3)
        total_fare4 = math.ceil(total_fare4)

        gst1 = math.ceil(gst1)
        gst2 = math.ceil(gst2)
        gst3 = math.ceil(gst3)
        gst4 = math.ceil(gst4)

        base_fare1 = math.ceil(base_fare1)
        base_fare2 = math.ceil(base_fare2)
        base_fare3 = math.ceil(base_fare3)
        base_fare4 = math.ceil(base_fare4)

        dis_fare1 = math.ceil(dis_fare1)
        dis_fare2 = math.ceil(dis_fare2)
        dis_fare3 = math.ceil(dis_fare3)
        dis_fare4 = math.ceil(dis_fare4)

        context = {
            # 'form_type': form_type,
            "booking_type": booking_type,
            "source": source,
            "destination": destination,
            "distance": distance,
            "total_fare1": total_fare1,
            "total_fare2": total_fare2,
            "total_fare3": total_fare3,
            "total_fare4": total_fare4,
            "date": date,
            "time": time,
            # "time": formatted_time,
            # 're_date': re_date,
            # 're_time': re_time,
            "gst1": gst1,
            "gst2": gst2,
            "gst3": gst3,
            "gst4": gst4,
            "base_fare1": base_fare1,
            "base_fare2": base_fare2,
            "base_fare3": base_fare3,
            "base_fare4": base_fare4,
            "dis_fare1": dis_fare1,
            "dis_fare2": dis_fare2,
            "dis_fare3": dis_fare3,
            "dis_fare4": dis_fare4,
        }

        request.session["trip_type"] = booking_type
        request.session["source"] = source
        request.session["destination"] = destination
        request.session["distance"] = distance
        request.session["total_fare1"] = total_fare1
        request.session["total_fare2"] = total_fare2
        request.session["total_fare3"] = total_fare3
        request.session["total_fare4"] = total_fare4

        request.session["date"] = date
        request.session["time"] = time
        # request.session['re_time'] = re_time
        # request.session['re_date'] = re_date

        request.session["gst1"] = gst1
        request.session["gst2"] = gst2
        request.session["gst3"] = gst3
        request.session["gst4"] = gst4

        request.session["base_fare1"] = base_fare1
        request.session["base_fare2"] = base_fare2
        request.session["base_fare3"] = base_fare3
        request.session["base_fare4"] = base_fare4

        request.session["dis_fare1"] = dis_fare1
        request.session["dis_fare2"] = dis_fare2
        request.session["dis_fare3"] = dis_fare3
        request.session["dis_fare4"] = dis_fare4

        return redirect("cab_list")

    return redirect("index")


def CAB(request):
    number = Number.objects.all()
    booking_type = request.session.get("booking_type")
    source = request.session.get("source")
    destination = request.session.get("destination")
    distance = request.session.get("distance")
    date = request.session.get("date")
    time = request.session.get("time")
    total_fare1 = request.session.get("total_fare1")
    total_fare2 = request.session.get("total_fare2")
    total_fare3 = request.session.get("total_fare3")
    total_fare4 = request.session.get("total_fare4")
    per_km_price2 = request.session.get("per_km_price2")
    current_time_in_india = timezone.localtime(timezone.now())

    gst1 = request.session.get("gst1")
    gst2 = request.session.get("gst2")
    gst3 = request.session.get("gst3")
    gst4 = request.session.get("gst4")

    base_fare1 = request.session.get("base_fare1")
    base_fare2 = request.session.get("base_fare2")
    base_fare3 = request.session.get("base_fare3")
    base_fare4 = request.session.get("base_fare4")
    dis_fare1 = request.session.get("dis_fare1")
    dis_fare2 = request.session.get("dis_fare2")
    dis_fare3 = request.session.get("dis_fare3")
    dis_fare4 = request.session.get("dis_fare4")

    context = {
        "number": number,
        "booking_type": booking_type,
        "source": source,
        "destination": destination,
        "distance": distance,
        "date": date,
        "time": time,
        "total_fare1": total_fare1,
        "total_fare2": total_fare2,
        "total_fare3": total_fare3,
        "total_fare4": total_fare4,
        "gst1": gst1,
        "gst2": gst2,
        "gst3": gst3,
        "gst4": gst4,
        "per_km_price2": per_km_price2,
        "base_fare1": base_fare1,
        "base_fare2": base_fare2,
        "base_fare3": base_fare3,
        "base_fare4": base_fare4,
        "dis_fare1": dis_fare1,
        "dis_fare2": dis_fare2,
        "dis_fare3": dis_fare3,
        "dis_fare4": dis_fare4,
        "current_time_in_india": current_time_in_india,
    }

    return render(request, "oneway/cab-list.html", context)


def CAB_DETAIL(request):
    email = Email.objects.all()
    active_coupons = Coupon.objects.filter(is_active=True)
    number = Number.objects.all()
    car_name = request.POST.get("car_name")
    similar = request.POST.get("similar")
    car_price = request.POST.get("car_price")
    dis_price = request.POST.get("dis_price")
    base_fare = request.POST.get("base_fare")
    gst = request.POST.get("gst")
    source = request.session.get("source")
    destination = request.session.get("destination")
    distance = request.session.get("distance")
    booking_type = request.session.get("booking_type")
    date = request.session.get("date")
    time = request.session.get("time")
    request.session["car_name"] = car_name
    request.session["car_price"] = car_price
    request.session["dis_price"] = dis_price
    request.session["gst"] = gst

    context = {
        "number": number,
        "source": source,
        "destination": destination,
        "distance": distance,
        "date": date,
        "time": time,
        "gst": gst,
        "base_fare": base_fare,
        "car_name": car_name,
        "similar": similar,
        "car_price": car_price,
        "dis_price": dis_price,
        "booking_type": booking_type,
        "active_coupons": active_coupons,
        "email": email,
    }
    return render(request, "oneway/cab-detail.html", context)


def CAB_BOOKING(request):
    number = Number.objects.all()
    if request.method == "POST":
        booking_type = request.POST.get("booking_type")
        pickup_address = request.POST.get("pickup_address")
        drop_address = request.POST.get("drop_address")
        total = request.POST.get("total")
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_b = request.POST.get("mobile_b")
        pickup_city = request.POST.get("pickup_city")
        drop_city = request.POST.get("drop_city")
        booking_id = request.POST.get("booking_id")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        time = request.POST.get("time")
        car_price = request.POST.get("car_price")
        paid = request.POST.get("paid")
        remark = request.POST.get("remark")
        gst_company = request.POST.get("gst_company")
        gst_number = request.POST.get("gst_number")
        alternative_number = request.POST.get("alternative_number")
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")
        distance = request.POST.get("distance")

        gst = request.session.get("gst")
        car_name = request.session.get("car_name")

        total_payment = total
        payment_amount = 0

        en = booking(
            name=name,
            email=email,
            mobile_b=mobile_b,
            pickup_city=pickup_city,
            drop_city=drop_city,
            pickup_address=pickup_address,
            drop_address=drop_address,
            booking_id=booking_id,
            amount=amount,
            gst=gst,
            date=date,
            time=time,
            car_name=car_name,
            remark=remark,
            gst_number=gst_number,
            gst_company=gst_company,
            alternative_number=alternative_number,
            total=None,
            paid_amount=None,
            remaining_amount=None,
            booking_type=booking_type,
            distance=distance,
        )
        en.save()
        booking_id = en.booking_id

        a = int(float(amount))
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        request.session["pickup_city"] = pickup_city
        request.session["total"] = total
        request.session["amount"] = amount
        request.session["booking_id"] = booking_id
        request.session["name"] = name
        request.session["money"] = money
        request.session["coupon_price"] = coupon_price
        request.session["coupon_code"] = coupon_code
        request.session["booking_type"] = booking_type
        request.session["gst_company"] = gst_company
        request.session["gst_number"] = gst_number
        request.session["alternative_number"] = alternative_number

        source = request.session.get("source")
        destination = request.session.get("destination")
        distance = request.session.get("distance")
        # total_fare = request.session.get('total_fare')
        date = request.session.get("date")
        time = request.session.get("time")

        dis_price = request.session.get("dis_price")
        car_price = request.session.get("car_price")

        context = {
            "number": number,
            "car_price": car_price,
            "source": source,
            "destination": destination,
            "distance": distance,
            "total": total,
            "date": date,
            "time": time,
            "name": name,
            "mobile_b": mobile_b,
            "email": email,
            "pickup_address": pickup_address,
            "drop_address": drop_address,
            "payment_amount": payment_amount,
            "booking_id": booking_id,
            "amount": amount,
            "money": money,
            "money1": money1,
            "money2": money2,
            "paid": paid,
            "car_name": car_name,
            "dis_price": dis_price,
            "coupon_price": coupon_price,
            "coupon_code": coupon_code,
            "booking_type": booking_type,
            "gst_company": gst_company,
            "gst_number": gst_number,
            "alternative_number": alternative_number,
        }
        return render(request, "oneway/cab-booking.html", context)


def CONFIRM(request, booking_id):
    number = Number.objects.all()
    try:
        bookings = booking.objects.get(booking_id=booking_id)
        user_email = bookings.email
        # booking_data = booking.objects.all()

        booking_details = {
            "booking_id": bookings.booking_id,
            "date": bookings.date,
            "time": bookings.time,
            "name": bookings.name,
            "mobile_b": bookings.mobile_b,
            "email": bookings.email,
            "pickup_city": bookings.pickup_city,
            "drop_city": bookings.drop_city,
            "pickup_address": bookings.pickup_address,
            "drop_address": bookings.drop_address,
            # "payment_amount": bookings.payment_amount,
            "amount": bookings.amount,
            # "paid": bookings.paid,
            # "car_name": bookings.car_name,
            "remark": bookings.remark,
            "car_name": bookings.car_name,
            "paid_amount": bookings.paid_amount,
            "remaining_amount": bookings.remaining_amount,
            "distance": bookings.distance,
            "booking_type": bookings.booking_type,
            "gst_company": bookings.gst_company,
            "gst_number": bookings.gst_number,
            "gst": bookings.gst,
            "alternative_number": bookings.alternative_number,
        }
        invoice_html = generate_invoice_html(booking_details)

        if invoice_html:
            # Send the invoice via email
            subject = "Your Invoice"
            message = "Please find your invoice below:"
            from_email = "sandeepgodbms@gmail.com"
            recipient_list = [user_email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = "html"  # Set the content type to HTML
            email.body = invoice_html  # Set the email body to the HTML content
            email.send()
        else:
            return HttpResponse("Failed to generate or send the invoice")
    except booking.DoesNotExist:
        return HttpResponse("Booking not found")

    trip_type = request.session.get("trip_type")
    source = request.session.get("source")
    destination = request.session.get("destination")
    booking_id = request.session.get("booking_id")
    name = request.session.get("name")
    money = request.session.get("money")
    date = request.session.get("date")
    amount = request.session.get("amount")
    car_name = request.session.get("car_name")
    car_price = request.session.get("car_price")
    coupon_price = request.session.get("coupon_price")
    coupon_code = request.session.get("coupon_code")
    booking_type = request.session.get("booking_type")
    distance = request.session.get("distance")
    paid_amount = request.session.get("paid_amount")
    remaining_amount = request.session.get("remaining_amount")
    gst_company = request.session.get("gst_company")
    gst_number = request.session.get("gst_number")
    gst = request.session.get("gst")
    alternative_number = request.session.get("alternative_number")

    Booking = booking.objects.get(booking_id=booking_id)

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = int(total) - b

        with transaction.atomic():
            Booking.paid_amount = paid
            Booking.total = total
            Booking.remaining_amount = rem_amount
            Booking.save()

            request.session["paid"] = paid
            request.session["rem_amount"] = rem_amount

        context = {
            "number": number,
            "source": source,
            "booking_id": booking_id,
            "destination": destination,
            "name": name,
            "money": money,
            "paid_amount": paid_amount,
            "remaining_amount": remaining_amount,
            "date": date,
            "paid": paid,
            "rem_amount": rem_amount,
            "car_name": car_name,
            "trip_type": trip_type,
            "amount": amount,
            "total": total,
            "coupon_price": coupon_price,
            "car_price": car_price,
            "coupon_code": coupon_code,
            "booking_type": booking_type,
            "distance": distance,
            "gst_company": gst_company,
            "gst_number": gst_number,
            "gst": gst,
            "alternative_number": alternative_number,
        }
        return render(request, "oneway/confirm.html", context)


def send_invoice_email(request, booking_id):
    number = Number.objects.all()

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = int(total) - b

    try:
        bookings = booking.objects.get(booking_id=booking_id)
        user_email = bookings.email
        # booking_data = booking.objects.all()

        booking_details = {
            "booking_id": bookings.booking_id,
            "date": bookings.date,
            "time": bookings.time,
            "name": bookings.name,
            "mobile_b": bookings.mobile_b,
            "email": bookings.email,
            "pickup_city": bookings.pickup_city,
            "drop_city": bookings.drop_city,
            "pickup_address": bookings.pickup_address,
            "drop_address": bookings.drop_address,
            "amount": bookings.amount,
            "remark": bookings.remark,
            "car_name": bookings.car_name,
            "paid_amount": bookings.paid_amount,
            "remaining_amount": bookings.remaining_amount,
            "booking_type": bookings.booking_type,
            "gst_company": bookings.gst_company,
            "gst_number": bookings.gst_number,
            "gst": bookings.gst,
            "alternative_number": bookings.alternative_number,
        }
        invoice_html = generate_invoice_html(booking_details)

        if invoice_html:
            # Send the invoice via email
            subject = "Your Invoice"
            message = "Please find your invoice below:"
            from_email = "booking@makemyryde.com"
            recipient_list = [user_email]

            email = EmailMessage(subject, message, from_email, recipient_list)
            email.content_subtype = "html"  # Set the content type to HTML
            email.body = invoice_html  # Set the email body to the HTML content
            email.send()

            return redirect("confirm")
        else:
            return HttpResponse("Failed to generate or send the invoice")
    except booking.DoesNotExist:
        return HttpResponse("Booking not found")


def PASSWORD(request):
    return render(request, "forgot-password.html")


def PROFILE(request):
    return render(request, "profile.html")


def PRIVACY(request):
    number = Number.objects.all()
    return render(request, "other/privacy&policy.html", {"number": number})


def refund(request):
    number = Number.objects.all()
    return render(request, "other/refund.html", {"number": number})


def terms(request):
    number = Number.objects.all()
    return render(request, "other/terms&conditions.html", {"number": number})


def aboutus(request):
    number = Number.objects.all()
    return render(request, "other/aboutus.html", {"number": number})


def contactus(request):
    emails = Email.objects.all()
    socials = Social.objects.all()
    number = Number.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("message")

        a = Contact(
            name=name,
            email=email,
            mobile=mobile,
            message=message,
        )
        a.save()

        subject = "New Contact Us Form Submission"
        message_body = (
            f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nMessage: {message}"
        )
        send_mail(
            subject,
            message_body,
            email,  # Use the user's email as the sender's email address
            ["info@makemyryde.com"],  # Recipient's email address
            fail_silently=False,
        )

        messages.success(request, "Thanks For Contacting Us.")

    return render(
        request,
        "other/contactus.html",
        {"number": number, "socials": socials, "emails": emails},
    )


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def route_detail(request, custom_url):
    number = Number.objects.all()
    cities = City.objects.all()
    route = get_object_or_404(Route, custom_url=custom_url)
    return render(
        request,
        "routes/oneway_route.html",
        {"route": route, "cities": cities, "number": number},
    )


def oneway_dynamic(request, custom_url):
    number = Number.objects.all()
    route = get_object_or_404(Oneway_routes, custom_url=custom_url)
    return render(
        request, "routes/oneway_route.html", {"route": route, "number": number}
    )


def oneway_route_list(request):
    number = Number.objects.all()
    routes = Oneway_routes.objects.all()
    return render(
        request, "routes/oneway_route_list.html", {"routes": routes, "number": number}
    )


def roundway_city_list(request):
    number = Number.objects.all()
    r_city = Roundway_routes.objects.values("roundway_city").distinct()
    return render(
        request, "routes/roundway_city_list.html", {"r_city": r_city, "number": number}
    )


def roundway_city_route(request, city):
    # roundway_city = Roundway_routes.objects.all()
    number = Number.objects.all()
    routes = Roundway_routes.objects.filter(roundway_city=city)
    return render(
        request,
        "routes/roundway_route_list.html",
        {"city": city, "routes": routes, "number": number},
    )


def route_detail(request, custom_url):
    number = Number.objects.all()
    route = get_object_or_404(Roundway_routes, custom_url=custom_url)
    return render(
        request, "routes/roundway_route.html", {"route": route, "number": number}
    )


# def oneway_route_list(request):
# cities = City.objects.all()
# return render(request, "routes/oneway_route_list.html", {"cities": cities})


# def oneway_city_routes(request, city_name):
# city = get_object_or_404(City, city=city_name)
# routes = Route.objects.filter(city=city)
# return render(
#    request, "routes/oneway_city_routes.html", {"city": city, "routes": routes}
# )


def otp(request):
    return render(request, "otp.html")


def logout_view(request):
    logout(request)
    return render(request, "index.html")


class OTPView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        username = request.POST.get("username")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password = request.POST.get(
            "password"
        )  # Specify the desired mobile number here
        otp = random.randint(
            100000, 999999
        )  # Generate OTP here or use a library like `pyotp`

        if User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number is already exists")
            return redirect("otp")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already exists")
            return redirect("otp")

        user, _ = User.objects.get_or_create(mobile=mobile)
        user.otp = otp
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        # Send OTP via 2Factor.in API
        api_key = "2d1d5168-1bb8-11ee-addf-0200cd936042"  # Replace with your 2Factor.in API key
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/{otp}/OTP+is+{otp}"
        response = requests.get(url)

        if response.status_code == 200:
            return render(request, "verify_otp.html", {"mobile": mobile})
        else:
            return render(request, "register.html", {"error": "Failed to send OTP"})


class OTPVerificationView(View):
    def post(self, request):
        mobile = request.POST.get("mobile")  # Specify the desired mobile number here
        otp = request.POST.get("otp")

        try:
            user = User.objects.get(mobile=mobile, otp=otp)
            # Perform further authentication or login logic here
            user.is_active = True  # Activate the user account
            user.save()

            user.otp = None
            user.save(update_fields=["is_active", "otp"])
            return render(request, "login.html")
        except User.DoesNotExist:
            return render(
                request, "index.html", {"mobile": mobile, "error": "Invalid OTP"}
            )

    def get(self, request):
        return render(request, "index.html")


def submit_form(request):
    if request.method == "POST":
        car_name = request.POST.get("car_name")
        similar = request.POST.get("similar")
        car_price = request.POST.get("car_price")
        dis_price = request.POST.get("dis_price")
        base_fare = request.POST.get("base_fare")

        # You can also perform other operations or save the data to the database if needed

        # Redirect to the next page (cab-detail) along with the form data as URL parameters
        return redirect(
            "/cab-detail/?car_name={}&similar={}&car_price={}&dis_price={}".format(
                car_name, similar, car_price, dis_price, base_fare
            )
        )
    return render(request, "cab-list.html")


def DEMO(request):
    return render(request, "demo.html")


def ERROR(request):
    return render(request, "other/error.html")


def INVOICE(request):
    return render(request, "oneway/invoice.html")


def generate_invoice_html(booking_details):
    template_path = "oneway/invoice.html"
    template = get_template(template_path)
    html = template.render(booking_details)
    return html


def footer(request):
    socials = Social.objects.all()
    return render(request, "include/footer.html", {"socials": socials})


def popular(request):
    number = Number.objects.all()
    return render(request, "other/popular.html", {"number": number})
