# Generated by Django 4.2.3 on 2023-10-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0022_local_booking_distance"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="image",
            field=models.ImageField(default="", upload_to="car_images/"),
        ),
    ]