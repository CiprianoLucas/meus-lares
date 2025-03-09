from django.db import models
from meus_lares.storages import PublicMediaStorage
from soft_components import SoftModel
from django.utils.translation import gettext_lazy as _

class State(models.Model):
    acronym = models.CharField(_("acronym"), max_length=2, primary_key=True)
    name = models.CharField(_("name"), max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.acronym})"


class City(models.Model):
    name = models.CharField(_("name"), max_length=50)
    state = models.ForeignKey(State,verbose_name=_("state"),  on_delete=models.CASCADE, to_field="acronym")

    def __str__(self):
        return self.name


class Condominium(SoftModel):
    name = models.CharField(_("name"), max_length=255)
    cep = models.CharField(_("cep"), max_length=8)
    city = models.ForeignKey(
        City,verbose_name=_("city"),  on_delete=models.DO_NOTHING, related_name="place_city"
    )
    neighborhood = models.CharField(_("neighborhood"), max_length=255)
    street = models.CharField(_("street"), max_length=255)
    number = models.CharField(_("number"), max_length=20, null=True)
    complement = models.CharField(_("complement"), max_length=255, null=True)
    profile_photo = models.ImageField(
        _("profile photo"), 
        upload_to="places/profile-photo/",
        blank=True,
        null=True,
        storage=PublicMediaStorage(),
    )

    def __str__(self):
        return self.name

    def temporary_url(self):
        return self.profile_photo.url if self.profile_photo else None

    class Meta:
        verbose_name = _("Condominium")
        verbose_name_plural = _("Condominiums")


class Apartment(SoftModel):
    condominium = models.ForeignKey(Condominium,verbose_name=_("condominium"),  on_delete=models.CASCADE)
    identifier = models.CharField(_("identifier"), max_length=255)
    profile_photo = models.ImageField(
        _("profile photo"), 
        upload_to="places/profile-photo/", blank=True, storage=PublicMediaStorage()
    )
    complement = models.CharField(_("complement"), max_length=255, null=True, blank=True)

    def __str__(self):
        return f'"{self.identifier}" {_("in")} "{self.condominium}"'

    def temporary_url(self):
        return self.profile_photo.url if self.profile_photo else None

    def delete(self, *args, user=None, **kwargs):
        ParkingSpace.objects.filter(apartment=self).update(apartment=None)
        super().delete(*args, user=user, **kwargs)

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")


class ParkingSpace(SoftModel):
    condominium = models.ForeignKey(Condominium,verbose_name=_("condominium"),  on_delete=models.CASCADE)
    identifier = models.CharField(_("identifier"), max_length=255)
    complement = models.CharField(_("complement"), max_length=255, null=True, blank=True)
    apartment = models.ForeignKey(
        Apartment,verbose_name=_("apartment"),  on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def __str__(self):
        return f'"{self.identifier}" {_("in")} "{self.condominium}"'

    class Meta:
        verbose_name = _("Parking space")
        verbose_name_plural = _("Parking space")


class SharedPlaces(SoftModel):
    condominium = models.ForeignKey(Condominium,verbose_name=_("condominium"),  on_delete=models.CASCADE)
    identifier = models.CharField(_("identifier"), max_length=255)
    capacity = models.PositiveIntegerField(_("capacity"), blank=True, null=True)
    is_reserveable = models.BooleanField(_("is reserveable"), default=True)
    clean_time = models.PositiveIntegerField(
        _("clean time"), 
        blank=True, null=True, help_text=_("Cleaning time, in minutes")
    )
    complement = models.CharField(_("complement"), max_length=255, null=True, blank=True)

    def __str__(self):
        return f'"{self.identifier}" {_("in")} "{self.condominium}"'

    class Meta:
        verbose_name = _("Shared space")
        verbose_name_plural = _("Shared spaces")
