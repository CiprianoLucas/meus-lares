# Generated by Django 5.1 on 2024-12-10 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("condo_files", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contractfiles",
            old_name="constract",
            new_name="contract",
        ),
    ]