# Generated by Django 4.2.3 on 2023-09-11 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
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
                ("city", models.CharField(default="", max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Route",
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
                ("source", models.CharField(max_length=100)),
                ("destination", models.CharField(max_length=100)),
                ("custom_url", models.SlugField(unique=True)),
                (
                    "city",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="routes.city",
                    ),
                ),
            ],
        ),
    ]
