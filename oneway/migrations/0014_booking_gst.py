# Generated by Django 4.2.3 on 2023-10-16 09:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("oneway", "0013_rename_car_type_booking_car_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="gst",
            field=models.CharField(default="", max_length=100),
        ),
    ]