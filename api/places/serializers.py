import re
from django.utils.translation import gettext_lazy as _
from relations.models import CondoStaff
from rest_framework import serializers
from soft_components.serializers import softModelSerializer

from .models import Apartment, City, Condominium, ParkingSpace, SharedPlaces


class CondominiumsSerializer(softModelSerializer):
    city_name = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        model = Condominium
        fields = [
            "id",
            "name",
            "number",
            "complement",
            "neighborhood",
            "street",
            "city",
            "cep",
            "city_name",
            "state",
            "profile_photo",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "city_name": {"read_only": True},
            "state": {"read_only": True},
        }

    def get_state(self, obj):
        if obj.city:
            return obj.city.state.acronym
        return None

    def get_city_name(self, obj):
        if obj.city:
            return obj.city.name
        return None

    def to_internal_value(self, initial_data):
        data = initial_data.copy()
        if data.get("cep", None):
            data["cep"] = re.sub(r"\D", "", data["cep"]).zfill(8)
        return super().to_internal_value(data)

    def create(self, data):
        user = self.context["request"].user
        condominium = super().create(data)
        condo_staff = CondoStaff(condominium=condominium, user=user, role="owner")
        condo_staff.save(user=user)
        return condominium


class ApartmentSerializer(softModelSerializer):
    class Meta:
        model = Apartment
        fields = [
            "id",
            "condominium",
            "identifier",
            "complement",
            "profile_photo",
            "is_active",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "complement": {"required": False, "allow_null": True},
            "profile_photo": {"required": False, "allow_null": True},
            "condominium": {"required": False, "allow_null": True},
        }


class BulkApartmentCreateSerializer(serializers.Serializer):
    condominium_id = serializers.UUIDField()
    apartments = ApartmentSerializer(many=True)

    def validate_condominium_id(self, value):
        if not Condominium.objects.filter(id=value).exists():
            raise serializers.ValidationError(_("Condominium does not exist"))
        return value

    def create(self, validated_data):
        condominium_id = validated_data["condominium_id"]
        apartments_data = validated_data["apartments"]

        condominium = Condominium.objects.get(id=condominium_id)

        apartments = [
            Apartment(
                condominium=condominium,
                identifier=apartment["identifier"],
                complement=apartment.get("complement", ""),
            )
            for apartment in apartments_data
        ]
        Apartment.objects.bulk_create(apartments)
        return apartments


class ParkingSerializer(softModelSerializer):
    apartment_details = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpace
        fields = [
            "id",
            "identifier",
            "complement",
            "apartment",
            "apartment_details",
            "condominium",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "complement": {"required": False, "allow_null": True},
            "condominium": {"required": False, "allow_null": True},
            "apartment": {"required": False, "allow_null": True},
            "apartment_identifier": {"read_only": True},
        }

    def get_apartment_details(self, obj: ParkingSpace):
        if obj.apartment:
            return {
                "identifier": obj.apartment.identifier,
                "id": obj.apartment.id
            }
        return None


class BulkParkCreateSerializer(serializers.Serializer):
    condominium_id = serializers.UUIDField()
    parks = ParkingSerializer(many=True)

    def validate_condominium_id(self, value):
        if not Condominium.objects.filter(id=value).exists():
            raise serializers.ValidationError(_("Condominium does not exist"))
        return value

    def create(self, validated_data):
        condominium_id = validated_data["condominium_id"]
        parks_data = validated_data["parks"]

        condominium = Condominium.objects.get(id=condominium_id)

        parks = [
            ParkingSpace(
                condominium=condominium,
                identifier=park["identifier"],
                complement=park.get("complement", ""),
                apartment=park.get("apartment"),
            )
            for park in parks_data
        ]
        ParkingSpace.objects.bulk_create(parks)
        return parks


class SharedPlacesSerializer(softModelSerializer):
    class Meta:
        model = SharedPlaces
        fields = [
            "id",
            "condominium",
            "identifier",
            "complement",
            "capacity",
            "clean_time",
            "is_reserveable",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "complement": {"required": False, "allow_null": True},
            "condominium": {"required": False, "allow_null": True},
            "is_reserveable": {"required": False, "allow_null": True},
            "clean_time": {"required": False, "allow_null": True},
            "capacity": {"required": False, "allow_null": True},
        }


class BulkSharedPlacesCreateSerializer(serializers.Serializer):
    condominium_id = serializers.UUIDField()
    shareds = SharedPlacesSerializer(many=True)

    def validate_condominium_id(self, value):
        if not Condominium.objects.filter(id=value).exists():
            raise serializers.ValidationError(_("Condominium does not exist"))
        return value

    def create(self, validated_data):
        condominium_id = validated_data["condominium_id"]
        shareds_data = validated_data["shareds"]

        condominium = Condominium.objects.get(id=condominium_id)

        shareds = [
            SharedPlaces(
                condominium=condominium,
                identifier=shared["identifier"],
                complement=shared.get("complement", ""),
                capacity=shared.get("capacity"),
                clean_time=shared.get("clean_time"),
                is_reserveable=shared.get("is_reserveable"),
            )
            for shared in shareds_data
        ]
        SharedPlaces.objects.bulk_create(shareds)
        return shareds


class CitySerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ["id", "name", "state"]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "state": {"read_only": True},
        }

    def get_state(self, obj):
        if obj.state:
            return obj.state.acronym
        return None


class FullAddressSerializer(serializers.Serializer):
    state = serializers.CharField()
    city = serializers.IntegerField(required=False, allow_null=True)
    neighborhood = serializers.CharField(required=False, allow_null=True)
    street = serializers.CharField(required=False, allow_null=True)
