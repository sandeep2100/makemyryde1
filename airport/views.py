import math

import googlemaps
from contact.models import Number
from coupon.models import Coupon
from customadmin.models import Email
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import render , HttpResponse
from django.template.loader import get_template

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
    per_km_prices = Airport_price.objects.first()
    base = Base_Airport.objects.first()
    number = Number.objects.all()
    if request.method == "POST":
        airport = request.POST.get("airport")
        address = request.POST.get("address")
        date = request.POST.get("date")
        time = request.POST.get("time")
        booking_type = request.POST.get("booking_type")

        distance = airport_distance(airport, address)
        distance = math.ceil(distance)

    if per_km_prices:
        per_km_price1 = float(per_km_prices.price1)
        per_km_price2 = float(per_km_prices.price2)
        per_km_price3 = float(per_km_prices.price3)
        per_km_price4 = float(per_km_prices.price4)
        per_km_price5 = float(per_km_prices.price5)
        per_km_price6 = float(per_km_prices.price6)
        per_km_price7 = float(per_km_prices.price7)
        per_km_price8 = float(per_km_prices.price8)

        if distance < 8:
            base_fare1 = float(base.base1)
            base_fare2 = float(base.base2)
            base_fare3 = float(base.base3)
            base_fare4 = float(base.base4)
        elif distance > 50:
            base_fare1 = distance * per_km_price5 + float(base.base1)
            base_fare2 = distance * per_km_price6 + float(base.base2)
            base_fare3 = distance * per_km_price7 + float(base.base3)
            base_fare4 = distance * per_km_price8 + float(base.base4)
        else:
            base_fare1 = distance * per_km_price1 + float(base.base1)
            base_fare2 = distance * per_km_price2 + float(base.base2)
            base_fare3 = distance * per_km_price3 + float(base.base3)
            base_fare4 = distance * per_km_price4 + float(base.base4)

        gst1 = base_fare1 * 0.05
        gst2 = base_fare2 * 0.05
        gst3 = base_fare3 * 0.05
        gst4 = base_fare4 * 0.05

        gst1 = math.ceil(gst1)
        gst2 = math.ceil(gst2)
        gst3 = math.ceil(gst3)
        gst4 = math.ceil(gst4)

        base_fare1 = math.ceil(base_fare1)
        base_fare2 = math.ceil(base_fare2)
        base_fare3 = math.ceil(base_fare3)
        base_fare4 = math.ceil(base_fare4)

        est_amount1 = base_fare1 + gst1
        est_amount2 = base_fare2 + gst2
        est_amount3 = base_fare3 + gst3
        est_amount4 = base_fare4 + gst4

        context = {
            "number": number,
            "airport": airport,
            "address": address,
            "distance": distance,
            "date": date,
            "time": time,
            "booking_type": booking_type,
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
        request.session["booking_type"] = booking_type
        request.session["base_fare1"] = base_fare1
        request.session["base_fare2"] = base_fare2
        request.session["base_fare3"] = base_fare3
        request.session["base_fare4"] = base_fare4

        request.session["date"] = date
        request.session["time"] = time

        return render(request, "airport/cab-list.html", context)


def airport_cab_detail(request):
    email = Email.objects.all()
    active_coupons = Coupon.objects.filter(is_active=True)
    number = Number.objects.all()
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
    booking_type = request.session.get("booking_type")

    context = {
        "number": number,
        "airport": airport,
        "address": address,
        "distance": distance,
        "date": date,
        "time": time,
        "booking_type": booking_type,
        "gst": gst,
        "base_fare": base_fare,
        "car_name": car_name,
        "similar": similar,
        "car_price": car_price,
        "dis_price": dis_price,
        "active_coupons": active_coupons,
        "email": email,
    }
    request.session["base_fare"] = base_fare
    request.session["car_name"] = car_name
    request.session["car_price"] = car_price
    return render(request, "airport/cab-detail.html", context)


def airport_cab_booking(request):
    number = Number.objects.all()
    if request.method == "POST":
        booking_type = request.POST.get("booking_type")
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
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")
        distance = request.POST.get("distance")

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
            booking_type=booking_type,
            alternative_number=alternative_number,
            total=None,
            paid_amount=None,
            remaining_amount=None,
            distance=distance,
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
            "number": number,
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
            "booking_type": booking_type,
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


def airport_confirm(request, booking_id):
    number = Number.objects.all()
    try:
        bookings = airport_booking.objects.get(booking_id=booking_id)
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
            "amount": bookings.amount,
            "remark": bookings.remark,
            "booking_type": bookings.booking_type,
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
    except airport_booking.DoesNotExist:
        return HttpResponse("Booking not found")

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

    Booking = airport_booking.objects.get(booking_id=booking_id)

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

        context = {
            "number": number,
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


def INVOICE(request):
    return render(request, "airport/invoice.html")


def generate_invoice_html(booking_details):
    template_path = "airport/invoice.html"
    template = get_template(template_path)
    html = template.render(booking_details)
    return html


def send_invoice_email(request, booking_id):
    try:
        bookings = airport_booking.objects.get(booking_id=booking_id)
        user_email = bookings.email
        # booking_data = booking.objects.all()

        booking_details = {
            "booking_id": bookings.booking_id,
            # "total": bookings.total,
            "date": bookings.date,
            "time": bookings.time,
            "name": bookings.name,
            "mobile_b": bookings.mobile_b,
            "email": bookings.email,
            # "pickup_city": bookings.pickup_city,
            # "drop_city": bookings.drop_city,
            # "pickup_address": bookings.pickup_address,
            # "drop_address": bookings.drop_address,
            # "payment_amount": bookings.payment_amount,
            "amount": bookings.amount,
            # "paid": bookings.paid,
            # "car_name": bookings.car_name,
            "remark": bookings.remark,
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

            return HttpResponse("Invoice sent successfully")
        else:
            return HttpResponse("Failed to generate or send the invoice")
    except airport_booking.DoesNotExist:
        return HttpResponse("Booking not found")
