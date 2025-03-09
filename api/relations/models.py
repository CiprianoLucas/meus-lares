from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from places.models import Apartment, Condominium, SharedPlaces
from soft_components import SoftModel
from users.models import User


class CondoTenant(SoftModel):
    apartment = models.ForeignKey(
        Apartment, verbose_name=_("apartment"), on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.DO_NOTHING)
    is_responsible = models.BooleanField(_("is responsible"), default=False)
    is_first_contact = models.BooleanField(_("is first contact"), default=False)
    notes = models.TextField(_("notes"), blank=True, null=True)

    @property
    def condominium(self):
        return self.apartment.condominium

    def __str__(self):
        pr = _("of")
        return f'{_("tenant")}: "{self.user}" {pr} {self.apartment}'

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
        ("owner", _("Owner")),
        ("manager", _("Manager")),
        ("vigilant", _("Vigilant")),
        ("doorman", _("Doorman")),
        ("caretaker", _("Caretaker")),
        ("cleaner", _("Cleaner")),
    ]
    condominium = models.ForeignKey(
        Condominium, verbose_name=_("condominium"), on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.DO_NOTHING)
    role = models.CharField(_("role"), max_length=10, choices=ROLE_CHOICES)
    notes = models.TextField(_("notes"), blank=True, null=True)

    def __str__(self):
        pr = _("of")
        return f'{self.role}: "{self.user}" {pr} "{self.condominium}"'

    class Meta:
        verbose_name = _("Condominium staff")
        verbose_name_plural = _("Condominium staff")


class CondoTenantContract(SoftModel):
    tenant = models.ForeignKey(
        CondoTenant, verbose_name=_("tenant"), on_delete=models.DO_NOTHING
    )
    start_date = models.DateField(
        _("start date"),
    )
    end_date = models.DateField(_("end date"), blank=True, null=True)
    terms = models.TextField(
        _("terms"),
    )

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")


class PlaceReservation(SoftModel):
    place = models.ForeignKey(
        SharedPlaces, verbose_name=_("place"), on_delete=models.CASCADE
    )
    tenant = models.ForeignKey(
        CondoTenant, verbose_name=_("tenant"), on_delete=models.CASCADE
    )
    date = models.DateField(
        _("date"),
    )
    start_time = models.TimeField(
        _("start time"),
    )
    end_time = models.TimeField(
        _("end time"),
    )

    class Meta:
        verbose_name = _("Space reservation")
        verbose_name_plural = _("Space reservations")
        ordering = ["date", "start_time"]

    def clean(self):
        conflit = PlaceReservation.objects.filter(
            place=self.place,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if conflit.exists():
            raise serializers.ValidationError(_("This time is already booked"))
        super().clean()


class Car(SoftModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    plate = models.CharField(_("plate"), max_length=7)
    brand = models.CharField(_("brand"), max_length=30)
    model = models.CharField(_("model"), max_length=30)
    color = models.CharField(_("color"), max_length=30)

    def __str__(self):
        return f"{self.brand} {self.model} {self.color}: {self.plate}"

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        ordering = ["created_at"]
