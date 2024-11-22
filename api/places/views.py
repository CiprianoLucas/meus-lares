from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Condominium, City
from .serializers import CondominiumsSerializer, UserCondominiumSerializer, CitySerializer, FullAddressSerializer
from .permissions import IsRepresentative
from django.shortcuts import get_object_or_404
from django.db.models import Q
from users.models import User
import httpx

class CondominiumCreateView(generics.CreateAPIView):
    queryset = Condominium.objects.filter(is_active=True)
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(representative=self.request.user)

class CondominiumDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Condominium.objects.filter(is_active=True)
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated, IsRepresentative]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CondominiumListForResidentsView(generics.ListAPIView):
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Condominium.objects.filter(Q(is_active=True) & Q(residents=user)).distinct()

class CondominiumListForUnionsAndRepresentativesView(generics.ListAPIView):
    serializer_class = CondominiumsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_union_ids = user.condominium_unions.values_list('id', flat=True)
        
        return Condominium.objects.filter(
                Q(is_active=True) &(
                Q(representative=user) | 
                Q(unions=user)
            )).distinct()
    
class ResidentCondominiumCreateView(APIView):
    serializer_class = UserCondominiumSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk_Condominium):
        Condominium = get_object_or_404(Condominium, pk=pk_Condominium)
        residents = Condominium.residents.all()
        serializer = self.serializer_class(residents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk_Condominium):
        Condominium = get_object_or_404(Condominium, pk=pk_Condominium)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=user_email)
            Condominium.residents.add(user)
            response = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResidentCondominiumRemoveView(APIView):
    serializer_class = UserCondominiumSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk_Condominium, pk_user):
        Condominium = get_object_or_404(Condominium, pk=pk_Condominium)
        user = get_object_or_404(User, pk=pk_user)
        Condominium.residents.remove(user)
        return Response({'detail': 'Resident removed successfully'}, status=status.HTTP_200_OK)

class UnionCondominiumCreateView(APIView):
    serializer_class = UserCondominiumSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        Condominium = get_object_or_404(Condominium, pk=pk)
        unions = Condominium.unions.all()
        serializer = self.serializer_class(unions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        Condominium = get_object_or_404(Condominium, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=user_email)
            Condominium.unions.add(user)
            response = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnionCondominiumRemoveRemoveView(APIView):
    serializer_class = UserCondominiumSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk_Condominium, pk_user):
        Condominium = get_object_or_404(Condominium, pk=pk_Condominium)
        user = get_object_or_404(User, pk=pk_user)
        Condominium.unions.remove(user)
        return Response({'detail': 'Unions removed successfully'}, status=status.HTTP_200_OK)
    

class CitiesView(APIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get(self,request, uf):
        cities = City.objects.filter(state__acronym=uf)
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FullAddressView(APIView):
    serializer_class = FullAddressSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        http_response = httpx.request("GET", url)
        result = http_response.json()
        if 'erro' in result:
            return Response({"cep": "Cep não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        city = City.objects.filter(Q(name=result['localidade']) & Q(state__acronym=result['uf'])).first()

        response = {
            "state": result['uf'],
            "city": city.id if city else None,
            "neighborhood": result['bairro'] if result['bairro'] else None,
            "street": result['logradouro'] if result['logradouro'] else None,
        }

        serializer = FullAddressSerializer(data=response)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
