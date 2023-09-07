from django.shortcuts import render
import googlemaps
import math
from .models import *


# Create your views here.
def airport_distance(airport, address):
    # Initialize Google Maps API client
    gmaps = googlemaps.Client(key="AIzaSyAX0OjsvGZFaLvdaYyOvaWvRmSpnEqVNIo")

    # Make API request to calculate distance
    response = gmaps.distance_matrix(airport, address, mode="driving")

    # Extract distance value from response
    distance = response["rows"][0]["elements"][0]["distance"]["value"]

    # Convert distance from meters to kilometers
    distance_km = distance / 1000

    return distance_km


def airport_cab(request):
    if request.method == "POST":
        airport = request.POST.get("airport")
        address = request.POST.get("address")
        date = request.POST.get("date")
        time = request.POST.get("time")
        selected_option = request.POST.get("selected_option")

        distance = airport_distance(airport, address)
        distance = math.ceil(distance)

        per_km_price1 = 15
        per_km_price2 = 20
        per_km_price3 = 25
        per_km_price4 = 30

        per_km_price5 = 12
        per_km_price6 = 14
        per_km_price7 = 16
        per_km_price8 = 22

        if distance < 8:
            base_fare1 = 499
            base_fare2 = 699
            base_fare3 = 999
            base_fare4 = 1499
        elif distance > 50:
            base_fare1 = distance * per_km_price5 + 499
            base_fare2 = distance * per_km_price6 + 699
            base_fare3 = distance * per_km_price7 + 999
            base_fare4 = distance * per_km_price8 + 1499
        else:
            base_fare1 = distance * per_km_price1 + 499
            base_fare2 = distance * per_km_price2 + 699
            base_fare3 = distance * per_km_price3 + 999
            base_fare4 = distance * per_km_price4 + 1499

        gst1 = base_fare1 * 0.05
        gst2 = base_fare2 * 0.05
        gst3 = base_fare3 * 0.05
        gst4 = base_fare4 * 0.05

        est_amount1 = base_fare1 - gst1
        est_amount2 = base_fare2 - gst2
        est_amount3 = base_fare3 - gst3
        est_amount4 = base_fare4 - gst4

        context = {
            "airport": airport,
            "address": address,
            "distance": distance,
            "date": date,
            "time": time,
            "selected_option": selected_option,
            "base_fare1": base_fare1,
            "base_fare2": base_fare2,
            "base_fare3": base_fare3,
            "base_fare4": base_fare4,
            "est_amount1": est_amount1,
            "est_amount2": est_amount2,
            "est_amount3": est_amount3,
            "est_amount4": est_amount4,
        }
        request.session["airport"] = airport
        request.session["address"] = address
        request.session["distance"] = distance
        request.session["selected_option"] = selected_option
        request.session["base_fare1"] = base_fare1
        request.session["base_fare2"] = base_fare2
        request.session["base_fare3"] = base_fare3
        request.session["base_fare4"] = base_fare4

        request.session["date"] = date
        request.session["time"] = time

        return render(request, "airport/cab-list.html", context)


def airport_cab_detail(request):
    car_name = request.POST.get("car_name")
    similar = request.POST.get("similar")
    car_price = request.POST.get("car_price")
    dis_price = request.POST.get("dis_price")
    base_fare = request.POST.get("base_fare")
    gst = request.POST.get("gst")

    airport = request.session.get("airport")
    address = request.session.get("address")
    distance = request.session.get("distance")
    date = request.session.get("date")
    time = request.session.get("time")
    selected_option = request.session.get("selected_option")

    context = {
        "airport": airport,
        "address": address,
        "distance": distance,
        "date": date,
        "time": time,
        "selected_option": selected_option,
        "gst": gst,
        "base_fare": base_fare,
        "car_name": car_name,
        "similar": similar,
        "car_price": car_price,
        "dis_price": dis_price,
    }
    request.session["base_fare"] = base_fare
    request.session["car_name"] = car_name
    request.session["car_price"] = car_price
    return render(request, "airport/cab-detail.html", context)


def airport_cab_booking(request):
    if request.method == "POST":
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
        car_name = request.POST.get("car_name")
        car_price = request.POST.get("car_price")
        paid = request.POST.get("paid")
        remark = request.POST.get("remark")
        flight_number = request.POST.get("flight_number")
        gst_company = request.POST.get("gst_company")
        gst_number = request.POST.get("gst_number")
        alternative_number = request.POST.get("alternative_number")
        selected_option = request.POST.get("selected_option")
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")

        en = airport_booking(
            name=name,
            email=email,
            mobile_b=mobile_b,
            pickup_city=pickup_city,
            drop_city=drop_city,
            booking_id=booking_id,
            amount=amount,
            date=date,
            time=time,
            remark=remark,
            flight_number=flight_number,
            gst_company=gst_company,
            gst_number=gst_number,
            selected_option=selected_option,
            alternative_number=alternative_number,
        )
        en.save()
        booking_id = en.booking_id

        total_payment = total
        payment_amount = 0

        a = int(amount)
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        source = request.session.get("source")
        destination = request.session.get("destination")
        distance = request.session.get("distance")
        date = request.session.get("date")
        time = request.session.get("time")
        car_name = request.session.get("car_name")
        base_fare = request.session.get("base_fare")

        context = {
            "pickup_city": pickup_city,
            "drop_city": drop_city,
            "car_name": car_name,
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
            "payment_amount": payment_amount,
            "booking_id": booking_id,
            "amount": amount,
            "money": money,
            "money1": money1,
            "money2": money2,
            "paid": paid,
            "base_fare": base_fare,
            "coupon_price": car_price,
            "coupon_code": coupon_code,
        }

        request.session["name"] = name
        request.session["mobile_b"] = mobile_b
        request.session["email"] = email
        request.session["booking_id"] = booking_id
        request.session["money"] = money
        request.session["pickup_city"] = pickup_city
        request.session["drop_city"] = drop_city
        request.session["coupon_price"] = coupon_price
        request.session["coupon_code"] = coupon_code

        return render(request, "airport/cab-booking.html", context)


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def airport_confirm(request):
    name = request.session.get("name")
    email = request.session.get("email")
    mobile = request.session.get("mobile")
    booking_id = request.session.get("booking_id")
    date = request.session.get("date")
    time = request.session.get("time")
    car_name = request.session.get("car_name")
    car_price = request.session.get("car_price")
    pickup_city = request.session.get("pickup_city")
    drop_city = request.session.get("drop_city")
    coupon_price = request.session.get("coupon_price")
    coupon_code = request.session.get("coupon_code")

    money = request.session.get("money")
    pick_up = request.session.get("pick_up")
    booking_type = request.POST.get("booking_type")

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = int(total) - b

        context = {
            "booking_id": booking_id,
            "name": name,
            "email": email,
            "money": money,
            "mobile": mobile,
            "time": time,
            "paid": paid,
            "date": date,
            "car_price": car_price,
            "car_name": car_name,
            "pick_up": pick_up,
            "rem_amount": rem_amount,
            "pickup_city": pickup_city,
            "drop_city": drop_city,
            "booking_type": booking_type,
            "total": total,
            "coupon_price": coupon_price,
            "coupon_code": coupon_code,
        }

        return render(request, "airport/confirm.html", context)
