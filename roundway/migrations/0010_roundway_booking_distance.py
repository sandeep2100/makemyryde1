# Generated by Django 4.2.3 on 2023-10-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("roundway", "0009_roundway_booking_booking_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="roundway_booking",
            name="distance",
            field=models.CharField(default="", max_length=200),
        ),
    ]