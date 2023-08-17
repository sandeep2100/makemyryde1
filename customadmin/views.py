from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from myapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from myapp.models import booking


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/dashboard/')

        if request.method == 'POST':
            email = request.method.get('email')
            password = request.method.get('password')
            user_obj = User.objects.filter(email=email)

            if not user_obj.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj = authenticate(email=email, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/dashboard/')

            messages.info(request, 'Invalid Password')
            return redirect('/')
        return render(request, 'login.html')
    except Exception as e:
        print(e)


def dashboard(request):
    return render(request, 'dashboard.html')


def bookings(request):
    objs = booking.objects.all()
    return render(request, 'booking.html', {'objs': objs})