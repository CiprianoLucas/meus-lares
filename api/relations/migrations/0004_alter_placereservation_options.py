# Generated by Django 5.1 on 2024-12-26 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("relations", "0003_placereservation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="placereservation",
            options={
                "ordering": ["date", "start_time"],
                "verbose_name": "Reserva de espaço",
                "verbose_name_plural": "Reservas de espaços",
            },
        ),
    ]