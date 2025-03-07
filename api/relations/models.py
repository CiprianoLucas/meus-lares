from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db import models
from places.models import Apartment, Condominium, SharedPlaces
from soft_components import SoftModel
from users.models import User


class CondoTenant(SoftModel):
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_responsible = models.BooleanField(default=False)
    is_first_contact = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    @property
    def condominium(self):
        return self.apartment.condominium

    def __str__(self):
        return f'tenant: "{self.user}" of {self.apartment}'

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        constraints = [
            models.UniqueConstraint(
                fields=["apartment", "user"],
                condition=models.Q(is_active=True),
                name="unique_active_tenant_per_apartment",
            )
        ]


class CondoStaff(SoftModel):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("vigilant", "Vigilant"),
        ("doorman", "Doorman"),
        ("caretaker", "Caretaker"),
        ("cleaner", "Cleaner"),
    ]
    condominium = models.ForeignKey(Condominium, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.role}: "{self.user}" of "{self.condominium}"'

    class Meta:
        verbose_name = "Colaborador do condomínio"
        verbose_name_plural = "Colaboradores do condomínio"


class CondoTenantContract(SoftModel):
    tenant = models.ForeignKey(CondoTenant, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    terms = models.TextField()

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"


class PlaceReservation(SoftModel):
    place = models.ForeignKey(SharedPlaces, on_delete=models.CASCADE)
    tenant = models.ForeignKey(CondoTenant, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "Reserva de espaço"
        verbose_name_plural = "Reservas de espaços"
        ordering = ["date", "start_time"]

    def clean(self):
        conflit = PlaceReservation.objects.filter(
            place=self.place,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if conflit.exists():
            raise serializers.ValidationError("This time is already booked.")
        super().clean()


class Car(SoftModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plate = models.CharField(max_length=7)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} {self.color}: {self.plate}"

    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        ordering = ["created_at"]
