from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Places
from .serializers import PlacesSerializer, UserPlaceSerializer
from .permissions import IsRepresentative
from django.shortcuts import get_object_or_404

class PlaceCreateView(generics.CreateAPIView):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

    def perform_create(self, serializer):
        serializer.save(
            representative=self.request.user,
            enabled=True
            )

class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    permission_classes = [IsRepresentative]

class PlaceListForResidentsView(generics.ListAPIView):
    serializer_class = PlacesSerializer

    def get_queryset(self):
        user = self.request.user
        return Places.objects.filter(residents=user)

class PlaceListForUnionsAndRepresentativesView(generics.ListAPIView):
    serializer_class = PlacesSerializer

    def get_queryset(self):
        user = self.request.user
        return Places.objects.filter(unions=user) | Places.objects.filter(representative=user)

    
class ResidentPlaceView(APIView):
    serializer_class = UserPlaceSerializer

    def get(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        residents = place.residents.all()
        serializer = self.serializer_class(residents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('id')
            place.residents.remove(user_id)
            return Response({'detail': 'Resident removed successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('id')
            place.residents.add(user_id)
            return Response({'detail': 'Resident added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnionPlaceView(APIView):
    serializer_class = UserPlaceSerializer

    def get(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        unions = place.unions.all()
        serializer = self.serializer_class(unions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('id')
            place.unions.remove(user_id)
            return Response({'detail': 'Resident removed successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        place = get_object_or_404(Places, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('id')
            place.unions.add(user_id)
            return Response({'detail': 'Resident added successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
