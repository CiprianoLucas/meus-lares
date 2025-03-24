from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soft_components.serializers import softModelSerializer

from .models import CondoTenant, CondoTenantContract, PlaceReservation


class CondoTenantSerializerList(softModelSerializer):
    user_details = serializers.SerializerMethodField()
    apartment_details = serializers.SerializerMethodField()

    class Meta:
        model = CondoTenant
        fields = [
            "id",
            "apartment",
            "apartment_details",
            "user",
            "user_details",
            "is_first_contact",
            "is_responsible",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "apartment": {"write_only": True},
            "user": {"write_only": True},
        }

    def get_user_details(self, obj: CondoTenant):
        user = obj.user
        result = {
            "full_name": user.full_name,
            "self_photo": user.self_photo.url if user.self_photo else None,
        }
        return result

    def get_apartment_details(self, obj: CondoTenant):
        apartment = obj.apartment
        result = {
            "id": apartment.id,
            "identifier": apartment.identifier,
            "condominium_details": {"name": apartment.condominium.name},
        }
        return result


class CondoTenantSerializer(softModelSerializer):
    user_details = serializers.SerializerMethodField()
    apartment_details = serializers.SerializerMethodField()

    class Meta:
        model = CondoTenant
        fields = [
            "id",
            "apartment",
            "apartment_details",
            "user",
            "user_details",
            "is_first_contact",
            "is_responsible",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "apartment": {"write_only": True},
            "user": {"write_only": True},
        }

    def get_user_details(self, obj: CondoTenant):
        user = obj.user
        result = {
            "full_name": user.full_name,
            "nick": user.nick,
            "cpf": user.cpf,
            "phone_number": user.phone_number,
            "email": user.email,
            "birth": user.birth,
            "verified_status": user.verified_status,
            "self_photo": user.self_photo.url if user.self_photo else None,
        }
        return result

    def get_apartment_details(self, obj: CondoTenant):
        apartment = obj.apartment
        result = {
            "id": apartment.id,
            "identifier": apartment.identifier,
            "condominium_details": {
                "name": apartment.condominium.name,
                "id": apartment.condominium.id,
            },
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
            raise serializers.ValidationError(_("This time is already booked"))
        return data
