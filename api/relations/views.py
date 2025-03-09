from soft_components.views import SoftModelsViewSet

from .models import CondoTenant, CondoTenantContract, PlaceReservation
from .serializers import (
    CondoTenantContractSerializer,
    CondoTenantSerializer,
    CondoTenantSerializerList,
    PlaceReservationSerializer,
)


class CondoTenantView(SoftModelsViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return CondoTenantSerializerList
        return CondoTenantSerializer

    def get_queryset(self):
        user = self.request.user
        relations = CondoTenant.objects.filter(
            apartment__condominium__condostaff__user=user,
            apartment__condominium__condostaff__role="owner",
        ).distinct()

        query_params = self.request.query_params
        apartment_id = query_params.get("apartment")
        if apartment_id:
            relations = relations.filter(apartment__id=apartment_id)

        is_active = query_params.get("is_active")
        if is_active:
            relations = relations.filter(is_active=True)

        return relations.select_related("user", "apartment", "apartment__condominium")


class CondoTenantContractView(SoftModelsViewSet):
    serializer_class = CondoTenantContractSerializer

    def get_queryset(self):
        user = self.request.user

        contracts = CondoTenantContract.objects.filter(
            content_type__model="condotenant"
        )
        user_contracts = [
            contract
            for contract in contracts
            if (
                contract.related_object.user == user
                or contract.related_object.apartment.condominium.condostaff_set.filter(
                    user=user, role__in=["owner"]
                ).exists()
            )
        ]

        return user_contracts


class PlaceReservationViewSet(SoftModelsViewSet):
    queryset = PlaceReservation.objects.all()
    serializer_class = PlaceReservationSerializer
