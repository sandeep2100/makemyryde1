from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import random


class User(AbstractUser):
    username = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100, unique=True)
    otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    is_mobile_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile']

class Cars(models.Model):
    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    car_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    seat = models.CharField(max_length=100)
    photo = models.FileField(upload_to='media/')
    created_date = models.DateTimeField(default=timezone.now)
    per_km_price = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        return self.car_name

class booking(models.Model):
    booking_id = models.CharField(max_length=100, unique=True, default='')
    pickup_city = models.CharField(max_length=100,default='')
    drop_city = models.CharField(max_length=100,default='')
    pickup_address = models.CharField(max_length=200)
    drop_address = models.CharField(max_length=200)
    mobile_b = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=100, default='')
    date = models.CharField(max_length=100, default='')
    time = models.CharField(max_length=100, default='')

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

            user = User.objects.create_user(username=username, email=email, mobile=mobile, password=password)
            user.save()

        if not self.booking_id:
            self.booking_id = generate_unique_booking_id()

        super(booking, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_booking_id():
    bi = str('MMR23')
    random_number = random.randint(10000, 99999)
    booking_id = f'{bi}-{random_number}'
    return booking_id


