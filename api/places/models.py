from django.db import models

from meus_lares.storages import PublicMediaStorage
from soft_components import SoftModel

class State(models.Model):
    acronym = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.acronym})"


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, to_field="acronym")

    def __str__(self):
        return self.name


class Condominium(SoftModel):
    name = models.CharField(max_length=255)
    cep = models.CharField(max_length=8)
    city = models.ForeignKey(
        City, on_delete=models.DO_NOTHING, related_name="place_city"
    )
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True)
    complement = models.CharField(max_length=255, null=True)
    profile_photo = models.ImageField(
        upload_to="places/profile-photo/", blank=True, storage=PublicMediaStorage()
    )

    def __str__(self):
        return self.name

    def temporary_url(self):
        return self.profile_photo.url if self.profile_photo else None

    class Meta:
        verbose_name = "Condomínio"
        verbose_name_plural = "Condomínios"


class Apartment(SoftModel):
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255)
    profile_photo = models.ImageField(
        upload_to="places/profile-photo/", blank=True, storage=PublicMediaStorage()
    )
    complement = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'"{self.identifier}" in "{self.condominium}"'

    def temporary_url(self):
        return self.profile_photo.url if self.profile_photo else None

    class Meta:
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"
        
class ParkingSpace(SoftModel):
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255)
    complement = models.CharField(max_length=255, null=True, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f'"{self.identifier}" in "{self.condominium}"'

    class Meta:
        verbose_name = "Vaga de estacionamento"
        verbose_name_plural = "Vagas de estacionamento"
        
class SharedPlaces(SoftModel):
    condominium = models.ForeignKey(Condominium, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    is_reserveable = models.BooleanField(default=True)
    clean_time = models.PositiveIntegerField(blank=True, null=True, help_text="Tempo para limpeza, em minutos")
    complement = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'"{self.identifier}" in "{self.condominium}"'

    class Meta:
        verbose_name = "Espaço compartilhado"
        verbose_name_plural = "Espaços compartilhados"
