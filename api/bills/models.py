from django.db import models
from soft_components import SoftModel
from relations.models import Contract

class RecurringFee(SoftModel):
    
    PAYMENT_STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('paid_delay', 'Paid with delay'),
        ('cancelled', 'Cancelled')
    ]
    
    name = models.CharField(max_length=50)
    break_penalizable = models.BooleanField(
        default=False,
        help_text="Será considerado no cálculo de multa de quebra de contrato"
    )
    delay_penalizable = models.BooleanField(
        default=False,
        help_text="Fará uma multa de atraso de pagamento"
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='waiting')
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    opening_day = models.DateField()
    due_date = models.DateField()
    
    class Meta:
        verbose_name = "Recorrência de pagamento"
        verbose_name_plural = "Recorrências de pagamento"

class BreachPenalty(SoftModel):
    name=models.CharField(max_length=50)
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    value = models.FloatField()
    is_percentage = models.BooleanField(
        default=False, 
        help_text="Multiplicará e somará as recorrências pendentes até fim do contrato pelo valor"
    )

    class Meta:
        verbose_name = "Multa de quebra de contrato do morador"
        verbose_name_plural = "Multas de quebra de contrato do morador"

class FinePenalty(SoftModel):
    INFRACTION_CHOICES = [
        ('delay_payment', 'Delay in payment'),
        ('noise', 'Excessive Noise'),
        ('illegal_parking', 'Illegal Parking'),
        ('safety_violation', 'Safety Violation'),
        ('trash', 'Improper Disposal of Trash'),
        ('break_rules', 'General Rule Violation'),
        ('damaged', 'Damaged infrastructure'),
        ('others', 'Others')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('disputed', 'Disputed'),
    ]
    
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=50)
    value = models.FloatField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    infraction_type = models.CharField(
        max_length=20, 
        choices=INFRACTION_CHOICES, 
        default='break_rules',
    )
    description = models.TextField()

    class Meta:
        verbose_name = "Multa do condomínio"
        verbose_name_plural = "Multas do condomínio"