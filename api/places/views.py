from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlacesSerializer, UserPlaceSerializer
from .permissions import IsRepresentative
from django.shortcuts import get_object_or_404
from django.db.models import Q
from users.models import User

class PlaceCreateView(generics.CreateAPIView):
    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlacesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(representative=self.request.user)

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.filter(is_active=True)
    serializer_class = PlacesSerializer
    permission_classes = [IsAuthenticated, IsRepresentative]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PlaceListForResidentsView(generics.ListAPIView):
    serializer_class = PlacesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Place.objects.filter(Q(is_active=True) & Q(residents=user)).distinct()

class PlaceListForUnionsAndRepresentativesView(generics.ListAPIView):
    serializer_class = PlacesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_union_ids = user.place_unions.values_list('id', flat=True)
        
        return Place.objects.filter(
                Q(is_active=True) &(
                Q(representative=user) | 
                Q(unions=user)
            )).distinct()
    
class ResidentPlaceCreateView(APIView):
    serializer_class = UserPlaceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk_place):
        place = get_object_or_404(Place, pk=pk_place)
        residents = place.residents.all()
        serializer = self.serializer_class(residents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk_place):
        place = get_object_or_404(Place, pk=pk_place)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=user_email)
            place.residents.add(user)
            response = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResidentPlaceRemoveView(APIView):
    serializer_class = UserPlaceSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk_place, pk_user):
        place = get_object_or_404(Place, pk=pk_place)
        user = get_object_or_404(User, pk=pk_user)
        place.residents.remove(user)
        return Response({'detail': 'Resident removed successfully'}, status=status.HTTP_200_OK)

class UnionPlaceCreateView(APIView):
    serializer_class = UserPlaceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        unions = place.unions.all()
        serializer = self.serializer_class(unions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get('email')
            user = get_object_or_404(User, email=user_email)
            place.unions.add(user)
            response = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnionPlaceRemoveRemoveView(APIView):
    serializer_class = UserPlaceSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk_place, pk_user):
        place = get_object_or_404(Place, pk=pk_place)
        user = get_object_or_404(User, pk=pk_user)
        place.unions.remove(user)
        return Response({'detail': 'Unions removed successfully'}, status=status.HTTP_200_OK)