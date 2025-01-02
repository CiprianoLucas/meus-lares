from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from places.models import Apartment, Condominium, SharedPlaces
from soft_components import SoftModel
from users.models import User


def contract_relation_validator(value: int | ContentType):
    if isinstance(value, ContentType):
        value = value.id
    allowed_models = {"condotenant", "condostaff"}
    model = ContentType.objects.get(id=value)

    if model.model not in allowed_models:
        raise ValidationError("This model is not correct")


class CondoTenant(SoftModel):
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_renter = models.BooleanField(default=False)
    is_responsible = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    contracts = GenericRelation("Contract")

    @property
    def condominium(self):
        return self.apartment.condominium

    def __str__(self):
        return f'tenant: "{self.user}" of {self.apartment}'

    class Meta:
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"


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


class Contract(SoftModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, validators=[contract_relation_validator]
    )
    object_id = models.UUIDField()
    related_object = GenericForeignKey("content_type", "object_id")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    terms = models.TextField()

    def __str__(self):
        return f"{self.content_type.model}-{self.related_object}"

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
            end_time__gt=self.start_time
        )
        if conflit.exists():
            raise ValidationError("This time is already booked.")
        super().clean()