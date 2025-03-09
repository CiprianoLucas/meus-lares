from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from soft_components import SoftAdmin

from .models import BreachPenalty, FinePenalty, RecurringFee


class RecurringFeeAdmin(SoftAdmin):
    list_display = (
        "name",
        "contract",
        "value",
        "payment_status",
        "opening_day",
        "due_date",
        "delay_penalizable",
        "break_penalizable",
    )
    list_filter = (
        "payment_status",
        "opening_day",
        "due_date",
        "delay_penalizable",
        "break_penalizable",
    )
    search_fields = ("value", "name")

    class Meta:
        verbose_name = _("Payment recurrence")
        verbose_name_plural = _("Payment Recurrences")


admin.site.register(RecurringFee, RecurringFeeAdmin)


class BreachPenaltyAdmin(SoftAdmin):
    list_display = ("name", "contract", "value", "is_percentage")
    list_filter = ("is_percentage",)
    search_fields = ("value", "name")

    class Meta:
        verbose_name = _("Breach of contract fine")
        verbose_name_plural = _("Breach of contract fines")


admin.site.register(BreachPenalty, BreachPenaltyAdmin)


class FinePenaltyAdmin(SoftAdmin):
    list_display = ("name", "contract", "value", "status", "infraction_type")
    list_filter = ("status", "infraction_type")
    search_fields = ("value", "name")

    class Meta:
        verbose_name = _("Condominium fine")
        verbose_name_plural = _("Condominium fines")


admin.site.register(FinePenalty, FinePenaltyAdmin)
