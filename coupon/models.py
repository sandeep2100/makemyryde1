from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(
        max_length=10, choices=[("percentage", "Percentage"), ("fixed", "Fixed Amount")]
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.code
