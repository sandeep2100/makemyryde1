# Generated by Django 4.2.3 on 2023-08-25 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("roundway", "0004_rename_roundway_roundway_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="roundway_booking",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="roundway_booking",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
