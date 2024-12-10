from rest_framework import serializers

from places.models import Apartment, Condominium
from soft_components.serializers import softModelSerializer

from .models import CondoStaff, CondoTenant


class CondoListSerializer(softModelSerializer):
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


class AptoListSerializer(softModelSerializer):
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
    user_fullname = serializers.SerializerMethodField()
    user_identity_photo = serializers.SerializerMethodField()
    apartment_identifier = serializers.SerializerMethodField()
    condominium_name = serializers.SerializerMethodField()
    condominium_neighborhood = serializers.SerializerMethodField()
    condominium_city = serializers.SerializerMethodField()
    condominium_state = serializers.SerializerMethodField()

    class Meta:
        model = CondoTenant
        fields = [
            "id",
            "apartment",
            "apartment_identifier",
            "condominium_name",
            "condominium_neighborhood",
            "condominium_city",
            "condominium_state",
            "user",
            "user_fullname",
            "user_identity_photo",
            "is_renter",
            "is_responsible",
            "notes",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_apartment_identifier(self, obj: CondoTenant):
        return obj.apartment.identifier

    def get_condominium_name(self, obj: CondoTenant):
        return obj.apartment.condominium.name

    def get_condominium_neighborhood(self, obj: CondoTenant):
        return obj.apartment.condominium.neighborhood

    def get_condominium_city(self, obj: CondoTenant):
        return obj.apartment.condominium.city.name

    def get_condominium_state(self, obj: CondoTenant):
        return obj.apartment.condominium.city.state.acronym

    def get_user_fullname(self, obj: CondoTenant):
        return obj.user.full_name

    def get_user_identity_photo(self, obj: CondoTenant):
        if obj.user.identity_photo:
            return obj.user.identity_photo
        return None


class CondoStaffSerializer(softModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    user_identity_photo = serializers.SerializerMethodField()
    condominium_name = serializers.SerializerMethodField()
    condominium_neighborhood = serializers.SerializerMethodField()
    condominium_city = serializers.SerializerMethodField()
    condominium_state = serializers.SerializerMethodField()

    class Meta:
        model = CondoStaff
        fields = [
            "id",
            "condominium",
            "condominium_name",
            "condominium_neighborhood",
            "condominium_city",
            "condominium_state",
            "user",
            "user_fullname",
            "user_identity_photo",
            "role",
            "notes",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_condominium_name(self, obj: CondoStaff):
        return obj.condominium.name

    def get_condominium_neighborhood(self, obj: CondoStaff):
        return obj.condominium.neighborhood

    def get_condominium_city(self, obj: CondoStaff):
        return obj.condominium.city.name

    def get_condominium_state(self, obj: CondoStaff):
        return obj.condominium.city.state.acronym

    def get_user_fullname(self, obj: CondoStaff):
        return obj.user.full_name

    def get_user_identity_photo(self, obj: CondoStaff):
        if obj.user.identity_photo:
            return obj.user.identity_photo
        return None
