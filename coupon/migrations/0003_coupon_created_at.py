# Generated by Django 4.2.3 on 2023-10-09 11:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("coupon", "0002_alter_coupon_expiration_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
