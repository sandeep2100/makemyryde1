# Generated by Django 4.2.3 on 2023-10-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("oneway", "0003_booking_booking_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="booking_type",
            field=models.CharField(default="Oneway Outstation", max_length=100),
        ),
    ]
