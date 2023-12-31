# Generated by Django 4.2.3 on 2023-08-14 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0006_remove_city_car_remove_city_package_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carpackage",
            name="car",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="local.car",
            ),
        ),
        migrations.AlterField(
            model_name="carpackage",
            name="package",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                to="local.package",
            ),
        ),
    ]
