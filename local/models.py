import random

from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from oneway.models import User


class local_booking(models.Model):
    car_name = models.CharField(max_length=100)
    booking_type = models.CharField(max_length=100)
    distance = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    booking_id = models.CharField(max_length=100, unique=True, default="")
    selected_city = models.CharField(max_length=100, default="")
    selected_package = models.CharField(max_length=100, default="")
    pick_up = models.CharField(max_length=200)
    remark = models.TextField()
    mobile_b = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    car_price = models.CharField(max_length=100, default="")
    date = models.CharField(max_length=100, default="")
    time = models.CharField(max_length=100, default="")
    amount = models.CharField(max_length=100, default="")
    estimated_amount = models.CharField(max_length=100, default="")
    gst_amount = models.CharField(max_length=100, default="")
    gst_company = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    alternative_number = models.CharField(max_length=100, null=True, blank=True)
    total = models.CharField(max_length=100, default="", null=True, blank=True)
    paid_amount = models.CharField(max_length=100, default="", null=True, blank=True)
    remaining_amount = models.CharField(
        max_length=100, default="", null=True, blank=True
    )

    def get_payment_status(self):
        try:
            amount = float(self.amount)
            paid_amount = float(self.paid_amount) if self.paid_amount else 0
        except (ValueError, TypeError):
            return "Invalid Amount"

        if paid_amount == 0:
            return "0 Rs Payment"
        elif paid_amount == amount:
            return "100% Payment"
        else:
            return "20% Payment"

    def save(self, *args, **kwargs):
        # Check if a user with the provided email already exists
        user = User.objects.filter(email=self.email).first()
        existing_user = User.objects.filter(mobile=self.mobile_b).first()

        if not user and not existing_user:
            # If no user exists with the provided email and mobile number, create a new user
            username = self.name  # Set the username as the mobile number
            mobile = self.mobile_b  # Generate a random password
            email = self.email
            password = make_password(None)

            user = User.objects.create_user(
                username=username, email=email, mobile=mobile, password=password
            )
            user.save()

        if not self.booking_id:
            self.booking_id = generate_unique_booking_id()
        super(local_booking, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_booking_id():
    bi = str("MMRLC")
    random_number = random.randint(10000, 99999)
    booking_id = f"{bi}-{random_number}"
    return booking_id


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="car_images/", default="")
    packages = models.ManyToManyField(Package, through="CarPackage")
    button = models.CharField(max_length=100, default="")
    container_image = models.ImageField(upload_to="local_images/", default="")
    car_name = models.CharField(max_length=100, default="")
    person_capacity = models.CharField(max_length=100, default="")
    bag_capacity = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class CarPackage(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.PROTECT)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.city.name} - {self.car.name} - {self.package.name}"
