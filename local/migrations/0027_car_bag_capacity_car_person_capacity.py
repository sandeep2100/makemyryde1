# Generated by Django 4.2.3 on 2023-10-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0026_car_car_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="bag_capacity",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="car",
            name="person_capacity",
            field=models.CharField(default="", max_length=100),
        ),
    ]