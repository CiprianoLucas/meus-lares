from rest_framework import serializers
from soft_components.serializers import softModelSerializer

from .models import (CondoStaff, CondoTenant, CondoTenantContract,
                     PlaceReservation)


class CondoTenantSerializerList(softModelSerializer):
    user = serializers.SerializerMethodField()
    apartment = serializers.SerializerMethodField()

    class Meta:
        model = CondoTenant
        fields = [
            "id",
            "apartment",
            "user"
            "is_first_contact",
            "is_responsible",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user(self, obj: CondoTenant):
        user = obj.user
        result = {
            "full_name": user.full_name,
            "self_photo": user.self_photo.url
        }
        return result

    def get_apartment(self, obj: CondoTenant):
        apartment = obj.apartment
        result = {
            "id": apartment.id,
            "identifier": apartment.identifier,
        }
        return result
    
class CondoTenantSerializer(softModelSerializer):
    user = serializers.SerializerMethodField()
    apartment = serializers.SerializerMethodField()

    class Meta:
        model = CondoTenant
        fields = [
            "id",
            "apartment",
            "user",
            "is_first_contact",
            "is_responsible",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user(self, obj: CondoTenant):
        user = obj.user
        result = {
            "full_name": user.full_name,
            "nick": user.nick,
            "cpf": user.cpf,
            "phone_number": user.phone_number,
            "email": user.email,
            "birth": user.birth,
            "verified_status": user.verified_status,
            "self_photo": user.self_photo.url
        }
        return result

    def get_apartment(self, obj: CondoTenant):
        apartment = obj.apartment
        result = {
            "id": apartment.id,
            "identifier": apartment.identifier,
            "condoninium": apartment.condominium.id,
            "condoninium_name": apartment.condominium.name,
        }
        return result

class CondoTenantContractSerializer(softModelSerializer):
    class Meta:
        model = CondoTenantContract
        fields = [
            "id",
            "content_type",
            "object_id",
            "start_date",
            "end_date",
            "terms",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "content_type": {"write_only": True},
            "object_id": {"write_only": True},
        }


class PlaceReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceReservation
        fields = ("place", "tenant", "date", "start_time", "end_time")

    def validate(self, data):
        place = data["place"]
        date = data["date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        conflit = PlaceReservation.objects.filter(
            place=place, date=date, start_time__lt=end_time, end_time__gt=start_time
        )
        if conflit.exists():
            raise serializers.ValidationError("This time is already booked.")
        return data
