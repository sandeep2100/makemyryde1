# Generated by Django 4.2.3 on 2023-10-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="airport_booking",
            name="booking_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]