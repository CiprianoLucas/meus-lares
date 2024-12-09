import re

from rest_framework import serializers

from relations.models import CondoStaff
from soft_components.serializers import softModelSerializer

from .models import Apartment, City, Condominium


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
        fields = ["id", "condominium", "identifier", "complement", "profile_photo"]
        extra_kwargs = {"id": {"read_only": True}}


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
