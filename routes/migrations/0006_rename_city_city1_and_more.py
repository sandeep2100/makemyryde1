# Generated by Django 4.2.3 on 2023-09-13 07:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("routes", "0005_local_city"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="City",
            new_name="City1",
        ),
        migrations.RenameModel(
            old_name="Local_City",
            new_name="Dynamic_Local_City",
        ),
    ]
