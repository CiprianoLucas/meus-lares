# Generated by Django 5.1 on 2025-01-02 18:37

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("places", "0005_alter_sharedplaces_capacity_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CondoRequest",
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
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(max_length=3000)),
                ("observations", models.JSONField(blank=True, default=list)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("complaint", "Complaint"),
                            ("repair", "Repair"),
                            ("others", "Others"),
                            ("reservation", "Reservation"),
                            ("payment_issue", "Payment Issue"),
                            ("noise_complaint", "Noise Complaint"),
                            ("security_issue", "Security Issue"),
                            ("lost_found", "Lost and Found"),
                            ("visitor_authorization", "Visitor Authorization"),
                            ("package_delivery", "Package Delivery"),
                            ("suggestion", "Suggestion"),
                            ("event", "Event"),
                            ("billing_question", "Billing Question"),
                            ("vehicle", "Vehicle"),
                        ],
                        default="others",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("canceled", "Canceled"),
                            ("awaiting_payment", "Awaiting Payment"),
                            ("rejected", "Rejected"),
                            ("awaiting_feedback", "Awaiting Feedback"),
                        ],
                        default="pending",
                    ),
                ),
                (
                    "apartment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="places.apartment",
                    ),
                ),
                (
                    "condominium",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="places.condominium",
                    ),
                ),
                (
                    "guardian",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="request_guardian",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="request_requester",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Requisição",
                "verbose_name_plural": "Requisições",
            },
        ),
    ]