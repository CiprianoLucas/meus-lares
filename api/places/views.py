import httpx
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from soft_components.views import SoftModelsViewSet

from .models import Apartment, City, Condominium, SharedPlaces
from .permissions import CondominiumOwnerPermission
from .serializers import (
    ApartmentSerializer,
    CitySerializer,
    SharedPlacesSerializer,
    CondominiumsSerializer,
    FullAddressSerializer,
)


class CondominiumOwnerView(SoftModelsViewSet):
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated, CondominiumOwnerPermission]

    def get_queryset(self):
        user = self.request.user
        condominiums = Condominium.objects.filter(
            condostaff__user=user, condostaff__role="owner"
        ).distinct()

        return condominiums


class ApartmentOwnerView(SoftModelsViewSet):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated, CondominiumOwnerPermission]

    def get_queryset(self):
        user = self.request.user

        apartments = Apartment.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        return apartments

class SharedPlacesView(SoftModelsViewSet):
    serializer_class = SharedPlacesSerializer

    def get_queryset(self):
        user = self.request.user

        places = SharedPlaces.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        return places

class CitiesStatesPagination(PageNumberPagination):
    page_size = 6000
    page_size_query_param = "page_size"

class CitiesView(APIView):
    serializer_class = CitySerializer
    pagination_class = CitiesStatesPagination

    def get(self, request, uf: str):
        cities = City.objects.filter(state__acronym=uf)
        paginator = self.pagination_class()
        paginated_cities = paginator.paginate_queryset(cities, request, view=self)
        serializer = self.serializer_class(paginated_cities, many=True)
        return paginator.get_paginated_response(serializer.data)


class FullAddressView(APIView):
    serializer_class = FullAddressSerializer

    def get(self, _, cep: str):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        http_response = httpx.request("GET", url)
        result = http_response.json()
        if "erro" in result:
            return Response(
                {"cep": "Cep não encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        city = City.objects.filter(
            Q(name=result["localidade"]) & Q(state__acronym=result["uf"])
        ).first()

        response = {
            "state": result["uf"],
            "city": city.id if city else None,
            "neighborhood": result["bairro"] if result["bairro"] else None,
            "street": result["logradouro"] if result["logradouro"] else None,
        }

        serializer = FullAddressSerializer(data=response)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
