# Generated by Django 4.2.3 on 2023-09-14 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0019_rename_local_city1_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="local_booking",
            name="paid_amount",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="local_booking",
            name="remaining_amount",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="local_booking",
            name="total",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
    ]
