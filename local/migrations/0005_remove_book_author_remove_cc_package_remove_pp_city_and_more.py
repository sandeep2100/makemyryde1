# Generated by Django 4.2.3 on 2023-08-14 11:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("local", "0004_alter_cc_package_alter_pp_city"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="author",
        ),
        migrations.RemoveField(
            model_name="cc",
            name="package",
        ),
        migrations.RemoveField(
            model_name="pp",
            name="city",
        ),
        migrations.DeleteModel(
            name="Author",
        ),
        migrations.DeleteModel(
            name="Book",
        ),
        migrations.DeleteModel(
            name="cc",
        ),
        migrations.DeleteModel(
            name="place",
        ),
        migrations.DeleteModel(
            name="pp",
        ),
    ]
