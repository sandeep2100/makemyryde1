import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class OnewayCityFix(models.Model):
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name


class OneWayRoute(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    # city_names = models.ForeignKey(OnewayCityFix, on_delete=models.CASCADE, default="")
    source_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    hatchback_price = models.IntegerField()
    sedan_price = models.IntegerField()
    suv_price = models.IntegerField()
    premium_price = models.IntegerField(default="0", null=True, blank=True)

    def __str__(self):
        return f"{self.source_city} to {self.destination_city}"


class Routes(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    heading2 = models.CharField(max_length=200)
    heading3 = models.CharField(max_length=200)
    heading4 = models.CharField(max_length=200)
    heading5 = models.CharField(max_length=200)
    heading6 = models.CharField(max_length=200)
    content = models.TextField()
    content2 = models.TextField()
    content3 = models.TextField()
    content4 = models.TextField()
    content5 = models.TextField()
    content6 = models.TextField()

    custom_url = models.SlugField(unique=True)

    def __str__(self):
        return self.custom_url


class User(AbstractUser):
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100, unique=True)
    otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    is_mobile_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]


class Cars(models.Model):
    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    car_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    seat = models.CharField(max_length=100)
    photo = models.FileField(upload_to="media/")
    created_date = models.DateTimeField(default=timezone.now)
    per_km_price = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        return self.car_name


class booking(models.Model):
    car_name = models.CharField(max_length=200, default="", null=True, blank=True)
    booking_type = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(default=timezone.now)
    booking_date = models.DateField(default=timezone.now)
    booking_id = models.CharField(max_length=100, unique=True)
    pickup_city = models.CharField(max_length=100, default="")
    drop_city = models.CharField(max_length=100, default="")
    pickup_address = models.CharField(max_length=200)
    drop_address = models.CharField(max_length=200)
    mobile_b = models.CharField(max_length=10)
    email = models.EmailField()
    gst = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=100, default="")
    date = models.CharField(max_length=100, default="")
    time = models.CharField(max_length=100, default="")
    remark = models.TextField(default="")
    distance = models.CharField(max_length=200, default="")
    gst_company = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    alternative_number = models.CharField(max_length=100, null=True, blank=True)

    # Payment-related fields
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

    # @staticmethod
    # def get_current_time_in_indian_timezone():
    #    tz = pytz.timezone("Asia/Kolkata")  # Indian Standard Time (IST)
    #     return timezone.now().astimezone(tz).time()

    # booking_time = models.TimeField(default=get_current_time_in_indian_timezone)

    def save(self, *args, **kwargs):
        # Check if a user with the provided email already exists
        user = User.objects.filter(email=self.email).first()
        existing_user = User.objects.filter(mobile=self.mobile_b).first()

        if not user and not existing_user:
            # If no user exists with the provided email and mobile number, create a new user
            username = self.name  # Set the username as the mobile number
            mobile = self.mobile_b  # Generate a random password
            email = self.email
            self.booking_date = timezone.now().date()
            self.booking_time = timezone.now().time()
            password = make_password(None)
            user = User.objects.create_user(
                username=username, email=email, mobile=mobile, password=password
            )
            user.save()

        if not self.booking_id:
            self.booking_id = generate_unique_booking_id()

        super(booking, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Confirm_Payment(models.Model):
# total = models.CharField(max_length=100)
# paid_amount = models.CharField(max_length=100)
# remaining_amount = models.CharField(max_length=100)


def generate_unique_booking_id():
    bi = str("MMRON")
    random_number = random.randint(10000, 99999)
    booking_id = f"{bi}-{random_number}"
    return booking_id


class PerKmPrices(models.Model):
    price1 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=100)
    price4 = models.CharField(max_length=100)


class OnewayPrice(models.Model):
    price1 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=100)
    price4 = models.CharField(max_length=100)
    price5 = models.CharField(max_length=100)
    price6 = models.CharField(max_length=100)
    price7 = models.CharField(max_length=100)
    price8 = models.CharField(max_length=100)
