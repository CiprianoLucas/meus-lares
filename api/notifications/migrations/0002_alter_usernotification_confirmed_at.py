# Generated by Django 5.1 on 2024-12-26 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usernotification",
            name="confirmed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
