# Generated by Django 5.1 on 2025-01-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("condo_requests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="condorequest",
            name="anonymous",
            field=models.BooleanField(default=False),
        ),
    ]