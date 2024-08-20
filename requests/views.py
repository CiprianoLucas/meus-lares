from rest_framework import generics
from .models import Request
from .serializers import RequestSerializer,RequestStatusSerializer
from rest_framework.exceptions import ValidationError
from .permissions import IsRequester, IsPendent
from django.db.models import Q

class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
        
class RequestListView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(
            Q(is_active=True) & ( 
            Q(place__unions=user) | 
            Q(place__representative=user))
            )


class RequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsRequester]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'P':
            raise ValidationError("Only requests with status 'PENDENTE' can be updated.")

        return super().update(request, *args, **kwargs)
    
class RequestStatusView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestStatusSerializer
    permission_classes = [IsPendent]
    
    
class RequestListForResidentsView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(Q(is_active=True) & Q(requester=user))

class RequestListForUnionsAndRepresentativesView(generics.ListAPIView):
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(Q(is_active=True) & Q(guardian=user))