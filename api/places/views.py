import httpx
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from soft_components.views import SoftPagination

from .models import Apartment, City, Condominium
from .permissions import CondominiumOwnerPermission
from .serializers import (
    ApartmentSerializer,
    CitySerializer,
    CondominiumsSerializer,
    FullAddressSerializer,
)


class CondominiumOwnerView(viewsets.ModelViewSet):
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated, CondominiumOwnerPermission]
    pagination_class = SoftPagination

    def get_queryset(self):
        user = self.request.user
        condominiums = Condominium.objects.filter(
            condostaff__user=user, condostaff__role="owner"
        ).distinct()

        return condominiums


class ApartmentOwnerView(viewsets.ModelViewSet):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated, CondominiumOwnerPermission]
    pagination_class = SoftPagination

    def get_queryset(self):
        user = self.request.user

        apartments = Apartment.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        condominium_id = self.request.query_params.get("condominium", None)
        if condominium_id:
            apartments = apartments.filter(condominium__id=condominium_id)

        return apartments


class CitiesView(APIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, uf):
        cities = City.objects.filter(state__acronym=uf)
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FullAddressView(APIView):
    serializer_class = FullAddressSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, cep):
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
