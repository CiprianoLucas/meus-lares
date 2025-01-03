# Generated by Django 5.1 on 2024-12-26 17:26

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0003_alter_parkingspace_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parkingspace",
            name="user",
        ),
        migrations.AddField(
            model_name="parkingspace",
            name="apartment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="places.apartment",
            ),
        ),
        migrations.CreateModel(
            name="SharedPlaces",
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
                ("identifier", models.CharField(max_length=255)),
                ("capacity", models.PositiveIntegerField()),
                ("is_reserveable", models.BooleanField(default=True)),
                (
                    "clean_time",
                    models.PositiveIntegerField(
                        help_text="Tempo para limpeza, em minutos"
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
                "verbose_name": "Espaço compartilhado",
                "verbose_name_plural": "Espaços compartilhados",
            },
        ),
    ]