import httpx
from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from soft_components.views import SoftModelsViewSet
from django.utils.translation import gettext_lazy as _
from .models import Apartment, City, Condominium, ParkingSpace, SharedPlaces
from .serializers import (ApartmentSerializer, BulkApartmentCreateSerializer,
                          BulkParkCreateSerializer,
                          BulkSharedPlacesCreateSerializer, CitySerializer,
                          CondominiumsSerializer, FullAddressSerializer,
                          ParkingSerializer, SharedPlacesSerializer)


class CondominiumOwnerView(SoftModelsViewSet):
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated]
    search = [
        "name__icontains",
        "city__name__icontains",
        "cep__icontains",
        "neighborhood__icontains",
        "street__icontains",
        "city__state__acronym",
    ]

    def get_queryset(self):
        user = self.request.user
        condominiums = Condominium.objects.filter(
            condostaff__user=user, condostaff__role="owner"
        ).distinct()

        condominiums = self.search_sort(condominiums)

        return condominiums


class ApartmentOwnerView(SoftModelsViewSet):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    sort = {"identifier": "identifier", "tenant_name": "condotenant__user__full_name"}
    search = [
        "identifier__icontains",
        "condotenant__user__full_name__icontains",
        "condotenant__user__email",
    ]

    def get_queryset(self):
        user = self.request.user

        apartments = Apartment.objects.filter(
            condominium__condostaff__user=user,
            condominium__condostaff__role__in=["owner"],
        ).distinct()

        query_params = self.request.query_params
        condominium_id = query_params.get("condominium")
        if condominium_id:
            apartments = apartments.filter(condominium__id=condominium_id)

        apartments = self.search_sort(apartments)

        return apartments

    def perform_update(self, serializer):
        instance = self.get_object()
        data = self.request.data

        if "is_active" in data and not data["is_active"]:
            if instance.condotenant_set.filter(is_active=True).exists():
                raise serializers.ValidationError(_(
                    "There are active residents in this apartment"
                ))

        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.condotenant_set.filter(is_active=True).exists():
            raise serializers.ValidationError(_(
                "There are active residents in this apartment"
            ))

        return super().destroy(request, *args, **kwargs)


class ApartmentByCondominiumView(APIView):

    def get(self, request, condominium_id):
        user = self.request.user

        apartments = Apartment.objects.filter(
            condominium__condostaff__user=user,
            condominium__condostaff__role__in=["owner"],
            condominium__id=condominium_id,
        ).distinct()

        results = [
            {"id": apartment.id, "identifier": apartment.identifier}
            for apartment in apartments
        ]

        response = {
            "results": results,
            "count": len(results),
            "next": None,
            "previous": None,
        }

        return Response(response)


class BulkApartmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BulkApartmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Apartments created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParkingView(SoftModelsViewSet):
    serializer_class = ParkingSerializer
    sort = {"identifier": "identifier", "apartment": "apartment__identifier"}
    search = [
        "identifier__icontains",
        "apartment__identifier__icontains",
    ]

    def get_queryset(self):
        user = self.request.user

        parks = ParkingSpace.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        query_params = self.request.query_params
        condominium_id = query_params.get("condominium")
        apartment_id = query_params.get("apartment")
        if condominium_id:
            parks = parks.filter(condominium__id=condominium_id)
        if apartment_id:
            parks = parks.filter(apartment__id=apartment_id)

        parks = self.search_sort(parks)

        return parks


class BulkParkCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BulkParkCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Parks created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SharedPlacesView(SoftModelsViewSet):
    serializer_class = SharedPlacesSerializer
    sort = {"identifier": "identifier", "capacity": "capacity"}
    search = ["identifier__icontains"]

    def get_queryset(self):
        user = self.request.user

        places = SharedPlaces.objects.filter(
            condominium__condostaff__user=user, condominium__condostaff__role="owner"
        ).distinct()

        condominium_id = self.request.query_params.get("condominium")
        if condominium_id:
            places = places.filter(condominium__id=condominium_id)

        places = self.search_sort(places)

        return places


class BulkSharedPlaceCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BulkSharedPlacesCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Parks created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
