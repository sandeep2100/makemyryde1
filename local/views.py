import math
from decimal import Decimal

from contact.models import Number
from coupon.models import Coupon
from customadmin.models import Email
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import render , HttpResponse
from django.template.loader import get_template

from .models import *


def invoice(request):
    return render(request, "local/invoice.html")


def local_cab(request):
    number = Number.objects.all()
    selected_city_id = request.session.get("selected_city_id")
    selected_package_id = request.session.get("selected_package_id")
    date = request.session.get("date")
    time = request.session.get("time")

    selected_city = City.objects.get(pk=selected_city_id)
    selected_package = Package.objects.get(pk=selected_package_id)

    # selected_car_packages = CarPackage.objects.filter(
    #     city_id=selected_city_id, package_id=selected_package_id
    # )
    car_packages = CarPackage.objects.filter(
        city_id=selected_city_id, package_id=selected_package_id
    )

    full_per = Decimal("0.15")
    gst_rate = Decimal("0.05")
    results = []
    for car_package in car_packages:
        car_name = car_package.car.name
        price = car_package.price
        amount = price * full_per
        dis_price = price + amount
        estimated_amount = price * (1 - gst_rate)
        gst_amount = price * gst_rate
        car_image_url = car_package.car.image.url
        button_label = car_package.car.button
        bags = car_package.car.bag_capacity
        person = car_package.car.person_capacity

        container_image = car_package.car.container_image.url
        custom_name = car_package.car.car_name

        estimated_amount = math.ceil(estimated_amount)
        gst_amount = math.ceil(gst_amount)
        price = math.ceil(price)
        dis_price = math.ceil(dis_price)

        results.append(
            {
                "car_name": car_name,
                "price": price,
                "car_image_url": car_image_url,
                "button_label": button_label,
                "container_image": container_image,
                "custom_name": custom_name,
                "estimated_amount": estimated_amount,
                "gst_amount": gst_amount,
                "dis_price": dis_price,
                "bags": bags,
                "person": person,
            }
        )

    return render(
        request,
        "local/cab-list.html",
        {
            "results": results,
            "number": number,
            "date": date,
            "time": time,
            "selected_city": selected_city,
            "selected_package": selected_package,
        },
    )


def local_cab_detail(request):
    email = Email.objects.all()
    active_coupons = Coupon.objects.filter(is_active=True)
    number = Number.objects.all()
    if request.method == "POST":
        selected_city = request.POST.get("selected_city")
        selected_package = request.POST.get("selected_package")
        car_name = request.POST.get("car_name")
        car_price = request.POST.get("car_price")
        gst = request.POST.get("gst")
        base_fare = request.POST.get("base_fare")

        request.session["base_fare"] = base_fare
        request.session["gst"] = gst
        request.session["selected_city"] = selected_city
        request.session["selected_package"] = selected_package
        request.session["car_price"] = car_price
        request.session["car_name"] = car_name
        date = request.session.get("date")
        time = request.session.get("time")

        context = {
            "number": number,
            "car_name": car_name,
            "car_price": car_price,
            "selected_city": selected_city,
            "selected_package": selected_package,
            "date": date,
            "time": time,
            "active_coupons": active_coupons,
            "email": email,
            "gst": gst,
            "base_fare": base_fare,
        }
        return render(request, "local/cab-detail.html", context)


def local_cab_booking(request):
    number = Number.objects.all()
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
        gst = request.session.get("gst")
        base_fare = request.session.get("base_fare")

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
            total=None,
            paid_amount=None,
            remaining_amount=None,
            car_name=car_name,
            gst_amount=gst,
            estimated_amount=base_fare,
        )
        en.save()
        booking_id = en.booking_id

        a = float(amount)
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        context = {
            "gst": gst,
            "number": number,
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
            "base_fare": base_fare,
            "alternative_number": alternative_number,
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
        request.session["car_name"] = car_name
        request.session["gst_company"] = gst_company
        request.session["gst_number"] = gst_number
        request.session["alternative_number"] = alternative_number

        return render(request, "local/cab-booking.html", context)


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def local_confirm(request, booking_id):
    number = Number.objects.all()
    try:
        bookings = local_booking.objects.get(booking_id=booking_id)
        user_email = bookings.email
        # booking_data = booking.objects.all()

        gst = request.session.get("gst")
        base_fare = request.session.get("base_fare")

        booking_details = {
            "base_fare": bookings.estimated_amount,
            "gst": bookings.gst_amount,
            "booking_id": bookings.booking_id,
            # "total": bookings.total,
            "date": bookings.date,
            "time": bookings.time,
            "name": bookings.name,
            "mobile_b": bookings.mobile_b,
            "email": bookings.email,
            "selected_city": bookings.selected_city,
            "selected_package": bookings.selected_package,
            "pick_up": bookings.pick_up,
            "amount": bookings.amount,
            # "paid": bookings.paid,
            # "car_name": bookings.car_name,
            "remark": bookings.remark,
            "car_name": bookings.car_name,
            "booking_type": bookings.booking_type,
            "gst_company": bookings.gst_company,
            "gst_number": bookings.gst_number,
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
    except local_booking.DoesNotExist:
        return HttpResponse("Booking not found")

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
    booking_type = request.session.get("booking_type")
    gst = request.session.get("gst")
    base_fare = request.session.get("base_fare")
    gst_company = request.session.get("gst_company")
    gst_number = request.session.get("gst_number")
    alternative_number = request.session.get("alternative_number")

    Booking = local_booking.objects.get(booking_id=booking_id)

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = float(total) - b

        with transaction.atomic():
            Booking.paid_amount = paid
            Booking.total = total
            Booking.remaining_amount = rem_amount
            Booking.save()

        context = {
            "base_fare": base_fare,
            "gst": gst,
            "number": number,
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
            "booking_type": booking_type,
            "gst_company": gst_company,
            "gst_number": gst_number,
            "alternative_number": alternative_number,
        }
        return render(request, "local/confirm.html", context)


def INVOICE(request):
    return render(request, "local/invoice.html")


def generate_invoice_html(booking_details):
    template_path = "local/invoice.html"
    template = get_template(template_path)
    html = template.render(booking_details)
    return html


def send_invoice_email(request, booking_id):
    try:
        bookings = local_booking.objects.get(booking_id=booking_id)
        user_email = bookings.email
        # booking_data = booking.objects.all()

        booking_details = {
            "base_fare": bookings.estimated_amount,
            "gst": bookings.gst_amount,
            "booking_id": bookings.booking_id,
            # "total": bookings.total,
            "date": bookings.date,
            "time": bookings.time,
            "name": bookings.name,
            "mobile_b": bookings.mobile_b,
            "email": bookings.email,
            "selected_city": bookings.selected_city,
            "selected_package": bookings.selected_package,
            "pick_up": bookings.pick_up,
            # "drop_address": bookings.drop_address,
            # "payment_amount": bookings.payment_amount,
            "amount": bookings.amount,
            # "paid": bookings.paid,
            "car_name": bookings.car_name,
            "remark": bookings.remark,
            "booking_type": bookings.booking_type,
            "gst_company": bookings.gst_company,
            "gst_number": bookings.gst_number,
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

            return HttpResponse("Invoice sent successfully")
        else:
            return HttpResponse("Failed to generate or send the invoice")
    except local_booking.DoesNotExist:
        return HttpResponse("Booking not found")
