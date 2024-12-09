from rest_framework import serializers

from places.models import Apartment, Condominium
from soft_components.serializers import softModelSerializer

from .models import CondoTenant


class CondoTenantListSerializer(softModelSerializer):
    city_name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = Condominium
        fields = [
            "id",
            "name",
            "neighborhood",
            "city_name",
            "state",
            "profile_photo",
        ]

    def get_state(self, obj: Condominium):
        return obj.city.state.acronym

    def get_city_name(self, obj: Condominium):
        return obj.city.name


class AptoTenantListSerializer(softModelSerializer):
    neighborhood = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    condominium = serializers.SerializerMethodField()
    condominium_name = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            "id",
            "identifier",
            "neighborhood",
            "city_name",
            "state",
            "condominium",
            "condominium_name",
            "profile_photo",
        ]

    def get_neighborhood(self, obj: Apartment):
        return obj.condominium.neighborhood

    def get_city_name(self, obj: Apartment):
        return obj.condominium.city.name

    def get_state(self, obj: Apartment):
        return obj.condominium.city.state.acronym

    def get_condominium(self, obj: Apartment):
        return obj.condominium.id

    def get_condominium_name(self, obj: Apartment):
        return obj.condominium.name


class CondoTenantSerializer(softModelSerializer):
    class Meta:
        model = CondoTenant
        fields = ["id", "apartment", "user", "is_renter", "is_responsible", "notes"]
        extra_kwargs = {"id": {"read_only": True}}
