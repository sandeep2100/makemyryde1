# Generated by Django 4.2.3 on 2023-09-13 06:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0018_rename_local_city_local_city1"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Local_City1",
            new_name="City",
        ),
    ]
