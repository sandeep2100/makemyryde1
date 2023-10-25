from airport.models import airport_booking, Airport_price, Base_Airport
from contact.models import Contact, Number
from coupon.forms import CouponForm
from coupon.models import Coupon
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from local.forms import RouteForm, CityForm, PackageForm, CarForm
from local.models import local_booking, CarPackage, City, Package, Car
from oneway.models import User, booking, OneWayRoute, PerKmPrices, OnewayPrice
from roundway.models import roundway_booking, PerKmPrices_r
from routes.models import Oneway_routes, Roundway_routes, Local_City

from .forms import SocialForm, EmailForm
from .models import *


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
    search_query = request.GET.get("q")

    if search_query:
        objs = objs.filter(
            Q(booking_id__icontains=search_query) | Q(mobile_b__icontains=search_query)
        )

    paginator = Paginator(objs, 10)
    page = request.GET.get("page")
    objs = paginator.get_page(page)

    return render(
        request,
        "admin/booking.html",
        {"objs": objs, "search_query": search_query},
    )


def roundway(request):
    search_query = request.GET.get("q")
    roundway = roundway_booking.objects.all().order_by("-created_at")

    if search_query:
        roundway = roundway.filter(
            Q(booking_id__icontains=search_query) | Q(mobile_b__icontains=search_query)
        )

    paginator = Paginator(roundway, 10)  # 10 items per page
    page = request.GET.get("page")
    roundway = paginator.get_page(page)

    return render(
        request,
        "admin/roundway.html",
        {"roundway": roundway, "search_query": search_query},
    )


def local(request):
    search_query = request.GET.get("q")
    local = local_booking.objects.all().order_by("-created_at")

    if search_query:
        local = local.filter(
            Q(booking_id__icontains=search_query) | Q(mobile_b__icontains=search_query)
        )

    paginator = Paginator(local, 10)  # 10 items per page
    page = request.GET.get("page")
    local = paginator.get_page(page)

    return render(
        request,
        "admin/local.html",
        {"local": local, "search_query": search_query},
    )


def airport(request):
    search_query = request.GET.get("q")
    airport_records = airport_booking.objects.all().order_by("-created_at")

    if search_query:
        airport_records = airport_records.filter(
            Q(booking_id__icontains=search_query) | Q(mobile_b__icontains=search_query)
        )

    paginator = Paginator(airport_records, 10)  # 10 items per page
    page = request.GET.get("page")
    airport = paginator.get_page(page)
    start_index = (airport.number - 1) * airport.paginator.per_page + 1

    return render(
        request,
        "admin/airport.html",
        {"airport": airport, "search_query": search_query, "start_index": start_index},
    )


def master_booking(request):
    objs = booking.objects.all().order_by("-created_at")
    local = local_booking.objects.all().order_by("-created_at")
    roundway = roundway_booking.objects.all().order_by("-created_at")
    airport = airport_booking.objects.all().order_by("-created_at")

    all_bookings = list(objs) + list(local) + list(roundway) + list(airport)
    all_bookings.sort(key=lambda x: x.created_at, reverse=True)

    search_query = request.GET.get("q")
    if search_query:
        all_bookings = [
            booking
            for booking in all_bookings
            if str(search_query).lower() in str(booking.mobile_b).lower()
            or str(search_query).lower() in str(booking.booking_id).lower()
        ]

    paginator = Paginator(all_bookings, 10)
    page = request.GET.get("page")
    all_bookings = paginator.get_page(page)

    return render(
        request,
        "admin/master_booking.html",
        {
            "all_bookings": all_bookings,
            "search_query": search_query,
        },
    )


def fix_routes(request):
    query = request.GET.get("q")
    routes = OneWayRoute.objects.all().order_by("-created_at")
    if query:
        routes = routes.filter(
            Q(source_city__icontains=query) | Q(destination_city__icontains=query)
        )

    paginator = Paginator(routes, 10)
    page = request.GET.get("page")
    routes = paginator.get_page(page)
    return render(
        request,
        "admin/fix_routes.html",
        {"routes": routes, "query": query},
    )


def edit_fix_route(request, route_id):
    route = get_object_or_404(OneWayRoute, id=route_id)

    if request.method == "POST":
        source_city = request.POST.get("source_city")
        destination_city = request.POST.get("destination_city")
        hatchback_price = request.POST.get("hatchback_price")
        sedan_price = request.POST.get("sedan_price")
        suv_price = request.POST.get("suv_price")
        premium_price = request.POST.get("premium_price")

        route.source_city = source_city
        route.destination_city = destination_city
        route.hatchback_price = hatchback_price
        route.sedan_price = sedan_price
        route.suv_price = suv_price
        route.premium_price = premium_price
        route.save()

        return redirect("fix_routes")
    return render(request, "admin/edit_fix_route.html", {"route": route})


def delete_fix_route(request, route_id):
    route = get_object_or_404(OneWayRoute, id=route_id)
    route.delete()
    return redirect("fix_routes")


def inquiry(request):
    query = request.GET.get("q")
    contact = Contact.objects.all().order_by("-created_at")

    if query:
        contact = Contact.filter(Q(name__icontains=query) | Q(email__icontains=query))

    paginator = Paginator(contact, 10)
    page = request.GET.get("page")
    contact = paginator.get_page(page)
    return render(request, "admin/inquiry.html", {"contact": contact})


def dynamic_number(request):
    numbers = Number.objects.all()
    return render(request, "admin/number.html", {"numbers": numbers})


def update_number(request, number_id):
    number = get_object_or_404(Number, pk=number_id)

    if request.method == "POST":
        new_number = request.POST.get("new_number")
        if new_number:
            number.number = new_number
            number.save()

    return redirect("number")


def coupon_list(request):
    coupons = Coupon.objects.all().order_by("-created_at")
    query = request.GET.get("q")
    if query:
        coupons = Coupon.filter(Q(code__icontains=query))

    return render(
        request, "admin/coupon_list.html", {"coupons": coupons, "query": query}
    )


def coupon_update(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect("coupon_list")
    else:
        form = CouponForm(instance=coupon)
    return render(request, "admin/coupon_update.html", {"form": form, "coupon": coupon})


def coupon_add(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("coupon_list")
    else:
        form = CouponForm()
    return render(request, "admin/coupon_add.html", {"form": form})


def cab_fare_airport(request):
    if request.method == "POST":
        price1 = request.POST.get("price1")
        price2 = request.POST.get("price2")
        price3 = request.POST.get("price3")
        price4 = request.POST.get("price4")
        price5 = request.POST.get("price5")
        price6 = request.POST.get("price6")
        price7 = request.POST.get("price7")
        price8 = request.POST.get("price8")

        base1 = request.POST.get("base1")
        base2 = request.POST.get("base2")
        base3 = request.POST.get("base3")
        base4 = request.POST.get("base4")

        base, created = Base_Airport.objects.get_or_create(id=1)
        base.base1 = base1
        base.base2 = base2
        base.base3 = base3
        base.base4 = base4

        per_km_prices, created = Airport_price.objects.get_or_create(id=1)
        per_km_prices.price1 = price1
        per_km_prices.price2 = price2
        per_km_prices.price3 = price3
        per_km_prices.price4 = price4
        per_km_prices.price5 = price5
        per_km_prices.price6 = price6
        per_km_prices.price7 = price7
        per_km_prices.price8 = price8
        per_km_prices.save()

        messages.success(request, "Prices updated successfully")

    per_km_prices = Airport_price.objects.first()
    base = Base_Airport.objects.first()
    return render(
        request,
        "admin/cab_fare_airport.html",
        {"per_km_prices": per_km_prices, "base": base},
    )


def airport_base(request):
    if request.method == "POST":
        base1 = request.POST.get("base1")
        base2 = request.POST.get("base2")
        base3 = request.POST.get("base3")
        base4 = request.POST.get("base4")

        base, created = Base_Airport.objects.get_or_create(id=1)
        base.base1 = base1
        base.base2 = base2
        base.base3 = base3
        base.base4 = base4
        base.save()

        base = Base_Airport.objects.first()
        per_km_prices = Airport_price.objects.first()
        messages.success(request, "Prices updated successfully")
        return render(
            request,
            "admin/cab_fare_airport.html",
            {"base": base, "per_km_prices": per_km_prices},
        )


def cab_fare(request):
    if request.method == "POST":
        price1 = request.POST.get("price1")
        price2 = request.POST.get("price2")
        price3 = request.POST.get("price3")
        price4 = request.POST.get("price4")

        # Update the prices in the database
        per_km_prices, created = PerKmPrices.objects.get_or_create(id=1)
        per_km_prices.price1 = price1
        per_km_prices.price2 = price2
        per_km_prices.price3 = price3
        per_km_prices.price4 = price4
        per_km_prices.save()

        messages.success(request, "Prices updated successfully")

    per_km_prices = PerKmPrices.objects.first()
    oneway_prices = OnewayPrice.objects.first()
    return render(
        request,
        "admin/cab_fare_oneway.html",
        {"per_km_prices": per_km_prices, "oneway_prices": oneway_prices},
    )


def OnewayCab(request):
    if request.method == "POST":
        price1 = request.POST.get("price1")
        price2 = request.POST.get("price2")
        price3 = request.POST.get("price3")
        price4 = request.POST.get("price4")

        price5 = request.POST.get("price5")
        price6 = request.POST.get("price6")
        price7 = request.POST.get("price7")
        price8 = request.POST.get("price8")

        # Update the prices in the database
        oneway_prices, created = OnewayPrice.objects.get_or_create(id=1)
        oneway_prices.price1 = price1
        oneway_prices.price2 = price2
        oneway_prices.price3 = price3
        oneway_prices.price4 = price4
        oneway_prices.price5 = price5
        oneway_prices.price6 = price6
        oneway_prices.price7 = price7
        oneway_prices.price8 = price8
        oneway_prices.save()
        oneway_prices = OnewayPrice.objects.first()
        per_km_prices = PerKmPrices.objects.first()
        return render(
            request,
            "admin/cab_fare_oneway.html",
            {"oneway_prices": oneway_prices, "per_km_prices": per_km_prices},
        )


def cab_fare_roundway(request):
    if request.method == "POST":
        price1 = request.POST.get("price1")
        price2 = request.POST.get("price2")
        price3 = request.POST.get("price3")
        price4 = request.POST.get("price4")

        # Update the prices in the database
        per_km_prices, created = PerKmPrices_r.objects.get_or_create(id=1)
        per_km_prices.price1 = price1
        per_km_prices.price2 = price2
        per_km_prices.price3 = price3
        per_km_prices.price4 = price4
        per_km_prices.save()

        messages.success(request, "Prices updated successfully")

    per_km_prices = PerKmPrices_r.objects.first()
    return render(
        request, "admin/cab_fare_roundway.html", {"per_km_prices": per_km_prices}
    )


def dynamic_page(request):
    routes = Oneway_routes.objects.all()
    search_query = request.GET.get("q")

    if search_query:
        routes = routes.filter(
            Q(source__icontains=search_query) | Q(destination__icontains=search_query)
        )

    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        custom_url = request.POST.get("custom_url")

        oneway_dynamic = Oneway_routes(
            source=source, destination=destination, custom_url=custom_url
        )
        oneway_dynamic.save()
    return render(
        request,
        "admin/dynamic_route.html",
        {"routes": routes, "search_query": search_query},
    )


def edit_dynamic_oneway(request, route_id):
    route = get_object_or_404(Oneway_routes, id=route_id)

    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        custom_url = request.POST.get("custom_url")

        # Update the existing route with new data
        route.source = source
        route.destination = destination
        route.custom_url = custom_url
        route.save()

        # Redirect to the list of routes after editing
        return redirect("dynamic_route")

    return render(request, "admin/edit_dynamic_oneway.html", {"route": route})


def delete_dynamic_oneway(request, route_id):
    route = get_object_or_404(Oneway_routes, id=route_id)
    route.delete()
    return redirect("dynamic_route")


def dynamic_roundway(request):
    routes = Roundway_routes.objects.all()
    search_query = request.GET.get("q")

    if search_query:
        routes = routes.filter(
            Q(source__icontains=search_query) | Q(destination__icontains=search_query)
        )

    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        city = request.POST.get("city")
        custom_url = request.POST.get("custom_url")

        roundway_dynamic = Roundway_routes(
            source=source,
            destination=destination,
            roundway_city=city,
            custom_url=custom_url,
        )
        roundway_dynamic.save()
    return render(
        request,
        "admin/dynamic_roundway.html",
        {"routes": routes, "search_query": search_query},
    )


def edit_dynamic_roundway(request, route_id):
    route = get_object_or_404(Roundway_routes, id=route_id)

    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        custom_url = request.POST.get("custom_url")

        # Update the existing route with new data
        route.source = source
        route.destination = destination
        route.custom_url = custom_url
        route.save()

        # Redirect to the list of routes after editing
        return redirect("dynamic_roundway")

    return render(request, "admin/edit_dynamic_roundway.html", {"route": route})


def delete_dynamic_roundway(request, route_id):
    route = get_object_or_404(Roundway_routes, id=route_id)
    route.delete()
    return redirect("dynamic_roundway")


def dynamic_local(request):
    routes = Local_City.objects.all()
    search_query = request.GET.get("q")

    if search_query:
        routes = routes.filter(
            Q(city_name__icontains=search_query) | Q(local_city__icontains=search_query)
        )

    if request.method == "POST":
        city_name = request.POST.get("city_name")
        local_city = request.POST.get("local_city")
        custom_url = request.POST.get("custom_url")

        local_dynamic = Local_City(
            city_name=city_name,
            local_city=local_city,
            custom_url=custom_url,
        )
        local_dynamic.save()
    return render(
        request,
        "admin/dynamic_local.html",
        {"routes": routes, "search_query": search_query},
    )


def edit_dynamic_local(request, route_id):
    route = get_object_or_404(Local_City, id=route_id)

    if request.method == "POST":
        city_name = request.POST.get("city_name")
        local_city = request.POST.get("local_city")
        custom_url = request.POST.get("custom_url")

        # Update the existing route with new data
        route.city_name = city_name
        route.local_city = local_city
        route.custom_url = custom_url
        route.save()

        return redirect("dynamic_local")
    return render(request, "admin/edit_dynamic_local.html", {"route": route})


def delete_dynamic_local(request, route_id):
    route = get_object_or_404(Local_City, id=route_id)
    route.delete()
    return redirect("dynamic_local")


def logo_settings_view(request):
    logo_settings = LogoSettings.objects.first()
    if request.method == "POST":
        logo_file = request.FILES.get("logo")
        if logo_file:
            if not logo_settings:
                logo_settings = LogoSettings()
            logo_settings.logo = logo_file
            logo_settings.save()
            return redirect(
                "admin:index"
            )  # Redirect to the admin index page or another suitable location
    return render(request, "admin/logo.html", {"logo_settings": logo_settings})


def edit_emails(request):
    email_instance = Email.objects.first()
    form = EmailForm(instance=email_instance)

    if request.method == "POST":
        form = EmailForm(request.POST, instance=email_instance)
        if form.is_valid():
            form.save()
            return redirect("email")

    return render(request, "admin/email.html", {"form": form})


def edit_social(request):
    social_instance = Social.objects.first()

    if request.method == "POST":
        form = SocialForm(request.POST, instance=social_instance)
        if form.is_valid():
            form.save()
            return redirect("edit_social")  # Redirect to a success page after saving
    else:
        form = SocialForm(instance=social_instance)

    return render(request, "admin/social_media.html", {"form": form})


def create_route(request):
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("route_list")
    else:
        form = RouteForm()
    return render(request, "admin/create_route.html", {"form": form})


def update_route(request, route_id):
    route = get_object_or_404(CarPackage, id=route_id)
    if request.method == "POST":
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect("route_list")
    else:
        form = RouteForm(instance=route)
    return render(request, "admin/update_route.html", {"form": form, "route": route})


def delete_route(request, route_id):
    route = get_object_or_404(CarPackage, id=route_id)
    if request.method == "POST":
        route.delete()
        return redirect("route_list")
    return render(request, "admin/delete_route.html", {"route": route})


def route_list(request):
    query = request.GET.get("q")
    routes = CarPackage.objects.all()
    if query:
        routes = routes.filter(
            Q(city__name__icontains=query)
            | Q(car__name__icontains=query)
            | Q(package__name__icontains=query)
        )
    page = request.GET.get("page")
    paginator = Paginator(routes, 10)
    routes = paginator.get_page(page)
    return render(request, "admin/route_list.html", {"routes": routes, "query": query})


def add_city(request):
    cities = City.objects.all()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route saved successfully.")
            return redirect(
                "route_list"
            )  # Redirect to the city list page after adding the city
    else:
        form = CityForm()

    if request.method == "POST" and "delete" in request.POST:
        city_id = request.POST.get("delete")
        city = get_object_or_404(City, id=city_id)
        city.delete()
        return redirect("route_list")

    if request.method == "POST" and "update" in request.POST:
        city_id = request.POST.get("update")
        city = get_object_or_404(City, id=city_id)
        form = CityForm(instance=city)

    return render(request, "admin/add_city.html", {"form": form, "cities": cities})


def add_package(request):
    packages = Package.objects.all()
    if request.method == "POST":
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "route_list"
            )  # Redirect to the city list page after adding the city
    else:
        form = PackageForm()

    if request.method == "POST" and "delete" in request.POST:
        package_id = request.POST.get("delete")
        package = get_object_or_404(Package, id=package_id)
        package.delete()
        return redirect("route_list")

    if request.method == "POST" and "update" in request.POST:
        package_id = request.POST.get("update")
        package = get_object_or_404(Package, id=package_id)
        form = PackageForm(instance=package)
    return render(
        request, "admin/add_package.html", {"packages": packages, "form": form}
    )


def add_car(request):
    cars = Car.objects.all()
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "route_list"
            )  # Redirect to the city list page after adding the city
    else:
        form = CarForm()

    if request.method == "POST" and "delete" in request.POST:
        car_id = request.POST.get("delete")
        car = get_object_or_404(Car, id=car_id)
        car.delete()
        return redirect("route_list")

    if request.method == "POST" and "update" in request.POST:
        car_id = request.POST.get("update")
        car = get_object_or_404(Car, id=car_id)
        form = CarForm(instance=car)
    return render(request, "admin/add_car.html", {"cars": cars, "form": form})


def popular_routes(request):
    routes = OneWayRoute.objects.all()
    success_message = None
    if request.method == "POST":
        source_city = request.POST.get("source_city")
        destination_city = request.POST.get("destination_city")
        hatchback_price = request.POST.get("hatchback_price")
        sedan_price = request.POST.get("sedan_price")
        suv_price = request.POST.get("suv_price")
        premium_price = request.POST.get("premium_price")

        existing_route = OneWayRoute.objects.filter(
            source_city=source_city, destination_city=destination_city
        ).first()
        if existing_route:
            existing_route.hatchback_price = hatchback_price
            existing_route.sedan_price = sedan_price
            existing_route.suv_price = suv_price
            existing_route.premium_price = premium_price
            existing_route.save()
        else:
            new_route = OneWayRoute(
                source_city=source_city,
                destination_city=destination_city,
                hatchback_price=hatchback_price,
                sedan_price=sedan_price,
                suv_price=suv_price,
                premium_price=premium_price,
            )
            new_route.save()

        success_message = (
            f"Route saved successfully from {source_city} to {destination_city}."
        )
    return render(
        request,
        "admin/popular_routes.html",
        {"success_message": success_message, "routes": routes},
    )
