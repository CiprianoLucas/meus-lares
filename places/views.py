from rest_framework import generics
from .models import Places
from .serializers import PlacesSerializer
from .permissions import IsRepresentative

class PlaceCreateView(generics.CreateAPIView):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer

    def perform_create(self, serializer):
        serializer.save(representative=self.request.user)

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
