from django.db import models
from django.utils.translation import gettext_lazy as _

from places.models import Apartment, Condominium
from soft_components import SoftModel
from users.models import User


class CondoRequest(SoftModel):
    TYPE_CHOICES = [
        ("complaint", _("Complaint")),
        ("repair", _("Repair")),
        ("others", _("Others")),
        ("reservation", _("Reservation")),
        ("payment_issue", _("Payment Issue")),
        ("noise_complaint", _("Noise Complaint")),
        ("security_issue", _("Security Issue")),
        ("lost_found", _("Lost and Found")),
        ("visitor_authorization", _("Visitor Authorization")),
        ("package_delivery", _("Package Delivery")),
        ("suggestion", _("Suggestion")),
        ("event", _("Event")),
        ("billing_question", _("Billing Question")),
        ("vehicle", _("Vehicle")),
    ]
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed")),
        ("canceled", _("Canceled")),
        ("awaiting_payment", _("Awaiting Payment")),
        ("rejected", _("Rejected")),
        ("awaiting_feedback", _("Awaiting Feedback")),
    ]
    requester = models.ForeignKey(
        User,
        verbose_name=_("requester"),
        on_delete=models.DO_NOTHING,
        related_name="request_requester",
    )
    guardian = models.ForeignKey(
        User,
        verbose_name=_("guardian"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="request_guardian",
    )
    condominium = models.ForeignKey(
        Condominium, verbose_name=_("condominium"), on_delete=models.CASCADE
    )
    apartment = models.ForeignKey(
        Apartment,
        verbose_name=_("apartment"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), max_length=3000)
    observations = models.JSONField(_("observations"), default=list, blank=True)
    type = models.CharField(_("type"), choices=TYPE_CHOICES, default="others")
    status = models.CharField(_("status"), choices=STATUS_CHOICES, default="pending")
    anonymous = models.BooleanField(_("anonymous"), default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")
