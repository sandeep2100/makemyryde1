from django.db import models
from django.contrib.auth.hashers import make_password
import random
from django.utils import timezone
from oneway.models import User


class airport_booking(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    selected_option = models.CharField(max_length=100, default="")
    booking_id = models.CharField(max_length=100, unique=True, default="")
    pickup_city = models.CharField(max_length=100, default="")
    drop_city = models.CharField(max_length=100, default="")
    mobile_b = models.CharField(max_length=10)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=100, default="")
    date = models.CharField(max_length=100, default="")
    time = models.CharField(max_length=100, default="")
    remark = models.TextField(default="")
    flight_number = models.CharField(max_length=100, null=True, blank=True)
    gst_company = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    alternative_number = models.CharField(max_length=100, null=True, blank=True)

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

        super(airport_booking, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def generate_unique_booking_id():
    bi = str("MMRAR")
    random_number = random.randint(10000, 99999)
    booking_id = f"{bi}-{random_number}"
    return booking_id
