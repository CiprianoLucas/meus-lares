from django.db import models
from soft_components import SoftModel
from places.models import Apartment, Condominium
from users.models import User


class CondoRequest(SoftModel):
    TYPE_CHOICES = [
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
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
        ("awaiting_payment", "Awaiting Payment"),
        ("rejected", "Rejected"),
        ("awaiting_feedback", "Awaiting Feedback"),
    ]
    requester = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="request_requester",
    )
    guardian = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="request_guardian",
    )
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=3000)
    observations = models.JSONField(default=list, blank=True)
    type = models.CharField(choices=TYPE_CHOICES, default="others")
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"



