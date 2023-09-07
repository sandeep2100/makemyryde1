# Generated by Django 4.2.3 on 2023-09-02 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=50, unique=True)),
                (
                    "discount_type",
                    models.CharField(
                        choices=[
                            ("percentage", "Percentage"),
                            ("fixed", "Fixed Amount"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "discount_value",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "expiration_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]