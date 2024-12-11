from rest_framework.permissions import IsAuthenticated

from places.models import Apartment, Condominium
from soft_components.views import SoftModelsViewSet

from .models import CondoStaff, CondoTenant, Contract
from .serializers import (
    AptoListSerializer,
    CondoListSerializer,
    CondoStaffSerializer,
    CondoTenantSerializer,
    ContractSerializer,
)


class CondoListView(SoftModelsViewSet):
    serializer_class = CondoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get("role", None)
        match role:
            case "tenant":
                user_role = {"apartment__condotenant__user": user}
            case _:
                user_role = {"condostaff__user": user, "condostaff__role": role}

        condominiuns = Condominium.objects.filter(**user_role).distinct()

        return condominiuns


class AptoListView(SoftModelsViewSet):
    serializer_class = AptoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        role = self.request.query_params.get("role", None)
        match role:
            case "tenant":
                user_role = {"condotenant__user": user}
            case _:
                user_role = {
                    "condominium__condostaff__user": user,
                    "condominium__condostaff__role": role,
                }

        apartments = Apartment.objects.filter(**user_role).distinct()
        return apartments


class CondoTenantView(SoftModelsViewSet):
    serializer_class = CondoTenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        relations = CondoTenant.objects.filter(
            apartment__condominium__condostaff__user=user,
            apartment__condominium__condostaff__role="owner",
        ).distinct()
        return relations


class CondoStaffView(SoftModelsViewSet):
    serializer_class = CondoStaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        relations = CondoStaff.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        condominium = self.request.query_params.get("condominium")
        condominium_name = self.request.query_params.get("condominium_name")
        condominium_city = self.request.query_params.get("condominium_city")
        condominium_state = self.request.query_params.get("condominium_state")
        role = self.request.query_params.get("role")
        user_fullname = self.request.query_params.get("user_fullname")
        if condominium:
            relations = relations.filter(condominium__id=condominium)
        if condominium_name:
            relations = relations.filter(condominium__name__icontains=condominium_name)
        if condominium_city:
            relations = relations.filter(
                condominium__city__name__icontains=condominium_city
            )
        if condominium_state:
            relations = relations.filter(
                condominium__city__state__acronym__iexact=condominium_state
            )
        if role:
            relations = relations.filter(role__iexact=role)
        if user_fullname:
            relations = relations.filter(user__full_name__icontains=user_fullname)

        return relations


class ContractTenantView(SoftModelsViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        contracts = Contract.objects.filter(content_type__model="condotenant")
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


class ContractStaffView(SoftModelsViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        contracts = Contract.objects.filter(content_type__model="condostaff")
        user_contracts = [
            contract
            for contract in contracts
            if (
                contract.related_object.user == user
                or contract.related_object.condominium.condostaff_set.filter(
                    user=user, role__in=["owner"]
                ).exists()
            )
        ]

        return user_contracts
