from rest_framework import generics
from .models import Request
from .serializers import RequestSerializer
from .permissions import IsGuardian, IsRequester

class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

class RequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user == self.get_object().guardian:
                return [IsGuardian()]
            elif self.request.user == self.get_object().requester:
                return [IsRequester()]
        return super().get_permissions()

class RequestListForRequesterView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(requester=user)

class RequestListForGuardianView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(guardian=user)
