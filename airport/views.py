from django.shortcuts import render


# Create your views here.
def airport_cab(request):
    return render(request, "airport/cab-list.html")


def airport_cab_detail(request):
    return render(request, "airport/cab-detail.html")


def airport_cab_booking(request):
    return render(request, "airport/cab-booking.html")


def airport_confirm(request):
    return render(request, "airport/confirm.html")
