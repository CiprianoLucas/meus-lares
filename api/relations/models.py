from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from places.models import Apartment, Condominium
from soft_components import SoftModel
from users.models import User


class CondoTenant(SoftModel):
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_renter = models.BooleanField(default=False)
    is_responsible = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

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
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
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
