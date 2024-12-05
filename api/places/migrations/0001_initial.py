# Generated by Django 5.1 on 2024-11-22 00:41

import uuid

import django.db.models.deletion
from django.db import migrations, models

import meus_lares.storages


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "acronym",
                    models.CharField(max_length=2, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Condominium",
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
                ("name", models.CharField(max_length=255)),
                ("cep", models.CharField(max_length=8)),
                ("neighborhood", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("number", models.CharField(max_length=20, null=True)),
                ("complement", models.CharField(max_length=255, null=True)),
                (
                    "profile_photo",
                    models.ImageField(
                        blank=True,
                        storage=meus_lares.storages.PublicMediaStorage(),
                        upload_to="places/profile-photo/",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="place_city",
                        to="places.city",
                    ),
                ),
            ],
            options={
                "verbose_name": "Condomínio",
                "verbose_name_plural": "Condomínios",
            },
        ),
        migrations.CreateModel(
            name="Apartment",
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
                ("identifier", models.CharField(max_length=255, null=True)),
                (
                    "profile_photo",
                    models.ImageField(
                        blank=True,
                        storage=meus_lares.storages.PublicMediaStorage(),
                        upload_to="places/profile-photo/",
                    ),
                ),
                ("complement", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "condominium",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="places.condominium",
                    ),
                ),
            ],
            options={
                "verbose_name": "Apartamento",
                "verbose_name_plural": "Apartamentos",
            },
        ),
        migrations.AddField(
            model_name="city",
            name="state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="places.state"
            ),
        ),
    ]
