# Generated by Django 4.2.3 on 2023-08-14 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0007_alter_carpackage_car_alter_carpackage_package"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carpackage",
            name="car",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="local.car"
            ),
        ),
        migrations.AlterField(
            model_name="carpackage",
            name="package",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="local.package"
            ),
        ),
    ]
