import math
from datetime import datetime

import googlemaps
from contact.models import Number
from coupon.models import Coupon
from customadmin.models import Email
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import render , redirect , HttpResponse
from django.template.loader import get_template

from .models import *


def calculate_distance(source1, destination1):
    # Initialize Google Maps API client
    gmaps = googlemaps.Client(key="AIzaSyAX0OjsvGZFaLvdaYyOvaWvRmSpnEqVNIo")

    # Make API request to calculate distance
    response = gmaps.distance_matrix(source1, destination1, mode="driving")

    # Extract distance value from response
    distance = response["rows"][0]["elements"][0]["distance"]["value"]

    # Convert distance from meters to kilometers
    distance_km = distance / 1000

    return distance_km


def calculate_day_difference(date, re_date):
    date_format = "%d/%b/%Y"  # Example: "10/Aug/2023"
    date = datetime.strptime(date, date_format)
    re_date = datetime.strptime(re_date, date_format)

    day_difference = (re_date - date).days + 1

    day_difference_km = day_difference * 300
    day_difference_fare = day_difference * 300

    return day_difference_fare


def calculate(request):
    per_km_prices = PerKmPrices_r.objects.first()
    number = Number.objects.all()
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        date = request.POST.get("date")
        return_date = request.POST.get("return_date")
        time1 = request.POST.get("time")

        time24 = time1
        time_obj = datetime.strptime(time24, "%H:%M")
        time = time_obj.strftime("%I:%M %p")

        distance = 2 * (calculate_distance(source, destination))
        toll_tax = distance

        day_difference_km = calculate_day_difference(date, return_date)

        if distance < day_difference_km:
            distance = day_difference_km
        else:
            distance = distance

        toll1 = distance - 100
        toll2 = distance + 100

        toll1 = math.ceil(toll1)
        toll2 = math.ceil(toll2)

    if per_km_prices:
        per_km_price1 = float(per_km_prices.price1)
        per_km_price2 = float(per_km_prices.price2)
        per_km_price3 = float(per_km_prices.price3)
        per_km_price4 = float(per_km_prices.price4)

        base_fare1 = distance * per_km_price1
        base_fare2 = distance * per_km_price2
        base_fare3 = distance * per_km_price3
        base_fare4 = distance * per_km_price4

        gst1 = base_fare1 * 0.05  # Add 5% GST amount
        gst2 = base_fare2 * 0.05
        gst3 = base_fare3 * 0.05
        gst4 = base_fare4 * 0.05

        day_difference_fare = calculate_day_difference(date, return_date)

        total_fare1 = base_fare1 + gst1
        total_fare2 = base_fare2 + gst2
        total_fare3 = base_fare3 + gst3
        total_fare4 = base_fare4 + gst4  # Add 5% GST amount

        total_fare1 += day_difference_fare
        total_fare2 += day_difference_fare
        total_fare3 += day_difference_fare
        total_fare4 += day_difference_fare

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
            "number": number,
            "source": source,
            "destination": destination,
            "distance": distance,
            "total_fare1": total_fare1,
            "total_fare2": total_fare2,
            "total_fare3": total_fare3,
            "total_fare4": total_fare4,
            "date": date,
            "time": time,
            "return_date": return_date,
            "per_km_price1": per_km_price1,
            "per_km_price2": per_km_price2,
            "per_km_price3": per_km_price3,
            "per_km_price4": per_km_price4,
            "toll1": toll1,
            "toll2": toll2,
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

        request.session["source"] = source
        request.session["destination"] = destination
        request.session["distance"] = distance
        request.session["toll1"] = toll1
        request.session["toll2"] = toll2

        request.session["total_fare1"] = total_fare1
        request.session["total_fare2"] = total_fare2
        request.session["total_fare3"] = total_fare3
        request.session["total_fare4"] = total_fare4

        request.session["per_km_price1"] = per_km_price1
        request.session["per_km_price2"] = per_km_price2
        request.session["per_km_price3"] = per_km_price3
        request.session["per_km_price4"] = per_km_price4

        request.session["date"] = date
        request.session["time"] = time
        request.session["return_date"] = return_date

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

        return redirect("round_cab")
    return redirect("index")


def round_cab(request):
    number = Number.objects.all()
    source = request.session.get("source")
    destination = request.session.get("destination")
    distance = request.session.get("distance")
    date = request.session.get("date")
    return_date = request.session.get("return_date")
    time = request.session.get("time")
    toll1 = request.session.get("toll1")
    toll2 = request.session.get("toll2")
    total_fare1 = request.session.get("total_fare1")
    total_fare2 = request.session.get("total_fare2")
    total_fare3 = request.session.get("total_fare3")
    total_fare4 = request.session.get("total_fare4")

    per_km_price1 = request.session.get("per_km_price1")
    per_km_price2 = request.session.get("per_km_price2")
    per_km_price3 = request.session.get("per_km_price3")
    per_km_price4 = request.session.get("per_km_price4")

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

    day_difference = calculate_day_difference(date, return_date)
    da = day_difference

    context = {
        "number": number,
        "source": source,
        "destination": destination,
        "distance": distance,
        "date": date,
        "return_date": return_date,
        "time": time,
        "toll1": toll1,
        "toll2": toll2,
        "total_fare1": total_fare1,
        "total_fare2": total_fare2,
        "total_fare3": total_fare3,
        "total_fare4": total_fare4,
        "per_km_price1": per_km_price1,
        "per_km_price2": per_km_price2,
        "per_km_price3": per_km_price3,
        "per_km_price4": per_km_price4,
        "da": da,
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

    return render(request, "roundway/cab-list.html", context)


def round_cab_detail(request):
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
    date = request.session.get("date")
    return_date = request.session.get("return_date")
    time = request.session.get("time")

    request.session["car_name"] = car_name
    request.session["car_price"] = car_price

    context = {
        "number": number,
        "source": source,
        "destination": destination,
        "distance": distance,
        "date": date,
        "time": time,
        "return_date": return_date,
        "gst": gst,
        "base_fare": base_fare,
        "car_name": car_name,
        "similar": similar,
        "car_price": car_price,
        "dis_price": dis_price,
        "active_coupons": active_coupons,
        "email": email,
    }

    return render(request, "roundway/cab-detail.html", context)


def round_cab_booking(request):
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
        return_date = request.POST.get("return_date")
        time = request.POST.get("time")
        car_name = request.POST.get("car_name")
        car_price = request.POST.get("car_price")
        paid = request.POST.get("paid")
        remark = request.POST.get("remark")
        gst_company = request.POST.get("gst_company")
        gst_number = request.POST.get("gst_number")
        alternative_number = request.POST.get("alternative_number")
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")
        distance = request.POST.get("distance")

        en = roundway_booking(
            name=name,
            email=email,
            mobile_b=mobile_b,
            pickup_city=pickup_city,
            drop_city=drop_city,
            pickup_address=pickup_address,
            drop_address=drop_address,
            booking_id=booking_id,
            amount=amount,
            date=date,
            return_date=return_date,
            time=time,
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

        total_payment = total
        payment_amount = 0

        a = int(amount)
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        request.session["booking_id"] = booking_id
        request.session["name"] = name
        request.session["money"] = money
        request.session["paid"] = paid
        request.session["total"] = total
        request.session["coupon_price"] = coupon_price
        request.session["coupon_code"] = coupon_code

        car_name = request.session.get("car_name")
        source = request.session.get("source")
        destination = request.session.get("destination")
        distance = request.session.get("distance")
        # total_fare = request.session.get('total_fare')
        date = request.session.get("date")
        time = request.session.get("time")
        return_date = request.session.get("return_date")
        # re_time = request.session.get('re_time')
        oneway_trip = request.session.get("oneway_trip")
        roundway_trip = request.session.get("roundway_trip")

        context = {
            "number": number,
            "car_name": car_name,
            "car_price": car_price,
            "source": source,
            "destination": destination,
            "distance": distance,
            "total": total,
            "date": date,
            "time": time,
            "return_date": return_date,
            # 're_time': re_time,
            "oneway_trip": oneway_trip,
            "roundway_trip": roundway_trip,
            "name": name,
            "mobile_b": mobile_b,
            "email": email,
            "pickup_address": pickup_address,
            "drop_address": drop_address,
            "payment_amount": payment_amount,
            "booking_id": booking_id,
            # 'total': float(total),
            "amount": amount,
            "h_date": date,
            # 'h_time' : time ,
            "money": money,
            "money1": money1,
            "money2": money2,
            "paid": paid,
            "coupon_price": coupon_price,
            "coupon_code": coupon_code,
            "booking_type": booking_type,
        }
        return render(request, "roundway/cab-booking.html", context)


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def round_confirm(request, booking_id):
    number = Number.objects.all()
    try:
        bookings = roundway_booking.objects.get(booking_id=booking_id)
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
            "pickup_city": bookings.pickup_city,
            "drop_city": bookings.drop_city,
            "pickup_address": bookings.pickup_address,
            "drop_address": bookings.drop_address,
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
        else:
            return HttpResponse("Failed to generate or send the invoice")
    except roundway_booking.DoesNotExist:
        return HttpResponse("Booking not found")

    source = request.session.get("source")
    destination = request.session.get("destination")
    booking_id = request.session.get("booking_id")
    name = request.session.get("name")
    money = request.session.get("money")
    paid = request.session.get("paid")
    date = request.session.get("date")
    days = request.session.get("days")
    car_name = request.session.get("car_name")
    total = request.session.get("total")
    coupon_price = request.session.get("coupon_price")
    car_price = request.session.get("car_price")
    car_code = request.session.get("car_code")

    Booking = roundway_booking.objects.get(booking_id=booking_id)

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
        "source": source,
        "destination": destination,
        "booking_id": booking_id,
        "name": name,
        "money": money,
        "paid": paid,
        "rem_amount": rem_amount,
        "date": date,
        "days": days,
        "car_name": car_name,
        "total": total,
        "coupon_price": coupon_price,
        "car_price": car_price,
        "coupon_code": coupon_price,
    }

    return render(request, "roundway/confirm.html", context)


def INVOICE(request):
    return render(request, "roundway/invoice.html")


def generate_invoice_html(booking_details):
    template_path = "roundway/invoice.html"  # Adjust the template path as needed
    template = get_template(template_path)
    html = template.render(booking_details)
    return html


def send_invoice_email(request, booking_id):
    try:
        bookings = roundway_booking.objects.get(booking_id=booking_id)
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
            "pickup_city": bookings.pickup_city,
            "drop_city": bookings.drop_city,
            "pickup_address": bookings.pickup_address,
            "drop_address": bookings.drop_address,
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
    except roundway_booking.DoesNotExist as e:
        # Add some error logging or debugging output
        print(f"Booking not found. Booking ID: {booking_id}. Error: {e}")
        return HttpResponse("Booking not found")
    except Exception as e:
        # Handle other exceptions and log them for further investigation
        print(f"An error occurred: {str(e)}")
        return HttpResponse("An error occurred")
