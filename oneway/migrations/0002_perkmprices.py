# Generated by Django 4.2.3 on 2023-09-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("oneway", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PerKmPrices",
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
                ("price1", models.CharField(max_length=100)),
                ("price2", models.CharField(max_length=100)),
                ("price3", models.CharField(max_length=100)),
                ("price4", models.CharField(max_length=100)),
            ],
        ),
    ]