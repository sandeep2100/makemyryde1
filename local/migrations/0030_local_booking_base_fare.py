# Generated by Django 4.2.3 on 2023-10-17 07:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0029_local_booking_gst_alter_local_booking_car_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="local_booking",
            name="base_fare",
            field=models.CharField(default="", max_length=100),
        ),
    ]
