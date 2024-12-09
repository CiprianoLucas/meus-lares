from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from places.models import Apartment, Condominium
from places.permissions import CondominiumOwnerPermission
from soft_components.views import SoftPagination

from .models import CondoTenant
from .serializers import (
    AptoTenantListSerializer,
    CondoTenantListSerializer,
    CondoTenantSerializer,
)


class CondoTenanListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CondoTenantListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SoftPagination

    def get_queryset(self):
        user = self.request.user
        condominiuns = Condominium.objects.filter(
            apartment__condotenant__user=user
        ).distinct()
        return condominiuns


class AptoTenanListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AptoTenantListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SoftPagination

    def get_queryset(self):
        user = self.request.user
        condominiuns = Apartment.objects.filter(condotenant__user=user).distinct()
        return condominiuns


class ApartmentTenantView(viewsets.ModelViewSet):
    serializer_class = CondoTenantSerializer
    permission_classes = [IsAuthenticated, CondominiumOwnerPermission]
    pagination_class = SoftPagination

    def get_queryset(self):
        user = self.request.user
        apartments = CondoTenant.objects.filter(user=user).distinct()
        return apartments
