from django.db import models
from django.utils.translation import gettext_lazy as _

from relations.models import CondoTenantContract
from soft_components import SoftModel


class RecurringFee(SoftModel):

    PAYMENT_STATUS_CHOICES = [
        ("waiting", _("Waiting")),
        ("pending", _("Pending")),
        ("paid", _("Paid")),
        ("overdue", _("Overdue")),
        ("paid_delay", _("Paid with delay")),
        ("cancelled", _("Cancelled")),
    ]

    name = models.CharField(_("name"), max_length=50)
    break_penalizable = models.BooleanField(
        _("break penalizable"),
        default=False,
        help_text=_(
            "It will be considered in the calculation of the "
            "fine for breach of contract"
        ),
    )
    delay_penalizable = models.BooleanField(
        _("delay penalizable"),
        default=False,
        help_text=_("Will charge a late payment fine"),
    )
    payment_status = models.CharField(
        _("payment status"),
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="waiting",
    )
    contract = models.ForeignKey(
        CondoTenantContract, verbose_name=_("contract"), on_delete=models.DO_NOTHING
    )
    value = models.FloatField(_("value"))
    opening_day = models.DateField(_("opening day"))
    due_date = models.DateField(_("due date"))

    class Meta:
        verbose_name = _("Payment recurrence")
        verbose_name_plural = _("Payment recurrences")


class BreachPenalty(SoftModel):
    name = models.CharField(_("name"), max_length=50)
    contract = models.ForeignKey(
        CondoTenantContract, verbose_name=_("contract"), on_delete=models.DO_NOTHING
    )
    value = models.FloatField(_("value"))
    is_percentage = models.BooleanField(
        _("is percentage"),
        default=False,
        help_text=_("It will multiply and add the pending recurrences"),
    )

    class Meta:
        verbose_name = _("Resident's breach of contract fine")
        verbose_name_plural = _("Resident's contract breach fines")


class FinePenalty(SoftModel):
    INFRACTION_CHOICES = [
        ("delay_payment", _("Delay in payment")),
        ("noise", _("Excessive Noise")),
        ("illegal_parking", _("Illegal Parking")),
        ("safety_violation", _("Safety Violation")),
        ("trash", _("Improper Disposal of Trash")),
        ("break_rules", _("General Rule Violation")),
        ("damaged", _("Damaged infrastructure")),
        ("others", _("Others")),
    ]
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("paid", _("Paid")),
        ("disputed", _("Disputed")),
    ]

    contract = models.ForeignKey(
        CondoTenantContract, verbose_name=_("contract"), on_delete=models.DO_NOTHING
    )
    name = models.CharField(_("name"), max_length=50)
    value = models.FloatField(
        _("value"),
    )
    status = models.CharField(
        _("status"), max_length=10, choices=STATUS_CHOICES, default="pending"
    )
    infraction_type = models.CharField(
        _("infraction type"),
        max_length=20,
        choices=INFRACTION_CHOICES,
        default="break_rules",
    )
    description = models.TextField(
        _("description"),
    )

    class Meta:
        verbose_name = _("Condominium fine")
        verbose_name_plural = _("Condominium fines")
