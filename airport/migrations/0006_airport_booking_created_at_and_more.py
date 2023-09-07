# Generated by Django 4.2.3 on 2023-08-25 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0005_remove_airport_booking_drop_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport_booking",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="airport_booking",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]