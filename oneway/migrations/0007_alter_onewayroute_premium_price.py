# Generated by Django 4.2.3 on 2023-10-05 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("oneway", "0006_booking_booking_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="onewayroute",
            name="premium_price",
            field=models.IntegerField(blank=True, default="0", null=True),
        ),
    ]