from django.shortcuts import render, redirect
import googlemaps
from datetime import datetime
import math
from django.views import View
from django.urls import reverse
from .models import *
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from local.models import City, Package, CarPackage
from coupon.models import Coupon
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import get_template
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from io import BytesIO
from django.core.mail import send_mail
from django.template.loader import render_to_string


@csrf_exempt
def validate_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")

        try:
            coupon = Coupon.objects.get(code=coupon_code)
            # Check if the coupon is valid (e.g., not expired)
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


def INDEX(request):
    cities = City.objects.all()
    packages = Package.objects.all()

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
                #  "selected_city": selected_city,
                # "selected_package": selected_package,
                "selected_car_packages": selected_car_packages,
                "date": date,
                "time": time,
            },
        )

    return render(request, "index.html", {"cities": cities, "packages": packages})


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
    # places = [
    #  "Mumbai, Maharashtra, India",
    #  "Silvassa, Dadra and Nagar Haveli and Daman and Diu, India",
    #  "Vapi, Gujarat, India",
    #  "Valsad, Gujarat, India",
    #  "Navsari, Gujarat, India",
    #  "Surat, Gujarat, India",
    #  "Bharuch, Gujarat, India",
    #  "Ankleshwar, Gujarat, India",
    #  "Vadodara, Gujarat, India",
    #  "Udaipur, Rajasthan, India",
    # ]

    if request.method == "POST":
        trip_type = request.POST.get("trip_type")
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

        per_km_price1 = 12
        per_km_price2 = 14
        per_km_price3 = 16
        per_km_price4 = 22

        if distance < 50:
            per_km_price1 = 40
            per_km_price2 = 45
            per_km_price3 = 50
            per_km_price4 = 60
        elif distance < 75:
            per_km_price1 = 30
            per_km_price2 = 35
            per_km_price3 = 40
            per_km_price4 = 45

        base_fare1 = distance * per_km_price1
        base_fare2 = distance * per_km_price2
        base_fare3 = distance * per_km_price3
        base_fare4 = distance * per_km_price4

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
            "trip_type": trip_type,
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
        print(trip_type)
        request.session["trip_type"] = trip_type
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
    trip_type = request.session.get("trip_type")
    source = request.session.get("source")
    destination = request.session.get("destination")
    distance = request.session.get("distance")
    date = request.session.get("date")
    time = request.session.get("time")
    total_fare1 = request.session.get("total_fare1")
    total_fare2 = request.session.get("total_fare2")
    total_fare3 = request.session.get("total_fare3")
    total_fare4 = request.session.get("total_fare4")
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
        "trip_type": trip_type,
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
    time = request.session.get("time")
    # re_date = request.session.get('re_date')
    # re_time = request.session.get('re_time')
    # base_fare = request.session.get('base_fare')

    request.session["car_name"] = car_name
    request.session["car_price"] = car_price
    request.session["dis_price"] = dis_price

    context = {
        "source": source,
        "destination": destination,
        "distance": distance,
        # 'total_fare': total_fare,
        "date": date,
        "time": time,
        # 're_date': re_date,
        # 're_time': re_time,
        "gst": gst,
        "base_fare": base_fare,
        # 'car': car,
        # 'car_type': car_type,
        # 'seat': seat,
        "car_name": car_name,
        "similar": similar,
        "car_price": car_price,
        "dis_price": dis_price,
    }
    return render(request, "oneway/cab-detail.html", context)


def CAB_BOOKING(request):
    if request.method == "POST":
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
        car_name = request.POST.get("car_name")
        car_price = request.POST.get("car_price")
        paid = request.POST.get("paid")
        remark = request.POST.get("remark")
        gst_company = request.POST.get("gst_company")
        gst_number = request.POST.get("gst_number")
        alternative_number = request.POST.get("alternative_number")
        coupon_price = request.POST.get("coupon_price")
        coupon_code = request.POST.get("coupon_code")

        en = booking(
            name=name,
            email=email,
            mobile_b=mobile_b,  # Assuming mobile_number is the field in the User model
            pickup_city=pickup_city,
            drop_city=drop_city,
            pickup_address=pickup_address,
            drop_address=drop_address,
            booking_id=booking_id,
            amount=amount,
            date=date,
            time=time,
            remark=remark,
            gst_number=gst_number,
            gst_company=gst_company,
            alternative_number=alternative_number,
        )
        en.save()
        booking_id = en.booking_id

        total_payment = total
        payment_amount = 0

        a = int(float(amount))
        money = a
        money1 = a * 0.2
        money1 = math.ceil(money1)
        money2 = 0

        request.session["total"] = total
        request.session["amount"] = amount
        request.session["booking_id"] = booking_id
        request.session["name"] = name
        request.session["money"] = money
        request.session["paid"] = paid
        request.session["coupon_price"] = coupon_price
        request.session["coupon_code"] = coupon_code

        source = request.session.get("source")
        destination = request.session.get("destination")
        distance = request.session.get("distance")
        # total_fare = request.session.get('total_fare')
        date = request.session.get("date")
        time = request.session.get("time")
        car_name = request.session.get("car_name")
        dis_price = request.session.get("dis_price")

        context = {
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
        }

        return render(request, "oneway/cab-booking.html", context)


def apply_discount(total, discount_amount):
    total = float(total)
    discount = float(discount_amount)
    discounted_total = total - discount
    return round(discounted_total, 2)


def CONFIRM(request):
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

    if request.method == "POST":
        paid = request.POST.get("paid")
        total = request.POST.get("total")

        request.session["paid"] = paid
        b = int(paid)
        rem_amount = int(total) - b

        context = {
            "source": source,
            "destination": destination,
            "booking_id": booking_id,
            "name": name,
            "money": money,
            "paid": paid,
            "rem_amount": rem_amount,
            "date": date,
            "car_name": car_name,
            "trip_type": trip_type,
            "amount": amount,
            "total": total,
            "coupon_price": coupon_price,
            "car_price": car_price,
            "coupon_code": coupon_code,
        }
        return render(request, "oneway/confirm.html", context)


def PASSWORD(request):
    return render(request, "forgot-password.html")


def PROFILE(request):
    return render(request, "profile.html")


def PRIVACY(request):
    return render(request, "privacy&policy.html")


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


def INVOICE(request):
    return render(request, "oneway/invoice.html")


def generate_invoice_html(booking_details):
    template_path = "oneway/invoice.html"
    template = get_template(template_path)
    html = template.render(booking_details)
    return html


def send_invoice_email(request, booking_id):
    try:
        bookings = booking.objects.get(booking_id=booking_id)
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
    except booking.DoesNotExist:
        return HttpResponse("Booking not found")
