# Generated by Django 5.1 on 2024-12-26 17:26

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0004_remove_parkingspace_user_parkingspace_apartment_and_more"),
        ("relations", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaceReservation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("history", models.JSONField(blank=True, default=list)),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="places.sharedplaces",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="relations.condotenant",
                    ),
                ),
            ],
            options={
                "ordering": ["date", "start_time"],
            },
        ),
    ]