from django.contrib import admin

from soft_components import SoftAdmin

from .models import BreachPenalty, RecurringFee, FinePenalty


class RecurringFeeAdmin(SoftAdmin):
    list_display = ("name", "contract", "value","payment_status", "opening_day", "due_date","delay_penalizable", "break_penalizable")
    list_filter = ("payment_status", "opening_day", "due_date", "delay_penalizable", "break_penalizable")
    search_fields = ("value", "name")

    class Meta:
        verbose_name = "Recorrência de pagamento"
        verbose_name_plural = "Recorrências de pagamento"

admin.site.register(RecurringFee, RecurringFeeAdmin)


class BreachPenaltyAdmin(SoftAdmin):
    list_display = ("name", "contract", "value", "is_percentage")
    list_filter = ("is_percentage",)
    search_fields = ("value", "name")

    class Meta:
        verbose_name = "Multa de quebra de contrato"
        verbose_name_plural = "Multas de quebra de contrato"

admin.site.register(BreachPenalty, BreachPenaltyAdmin)

class FinePenaltyAdmin(SoftAdmin):
    list_display = ("name", "contract", "value", "status", "infraction_type")
    list_filter = ("status","infraction_type")
    search_fields = ("value", "name")

    class Meta:
        verbose_name = "Multa de condomínio"
        verbose_name_plural = "Multas de condomínio"

admin.site.register(FinePenalty, FinePenaltyAdmin)