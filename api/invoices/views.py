from rest_framework import viewsets
from .models import RelationInvoice, Invoice
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from .permissions import IsRepresentative
from .serializers import RelationInvoiceSerializer, InvoicesSerializer
from django.db.models import Q

class RelationInvoiceViewSet(viewsets.ModelViewSet):
    queryset = RelationInvoice.objects.all()
    serializer_class = RelationInvoiceSerializer
    permission_classes = [IsRepresentative]
    
    def get_queryset(self):
        user = self.request.user
        return RelationInvoice.objects.filter(
            Q(is_active=True) & (
            Q(place__representative=user) |
            Q(place__unions=user))
            ).distinct()
    
    def perform_create(self, serializer):
        resident = serializer.validated_data['resident']
        place = serializer.validated_data['place']

        if not place.residents.filter(id=resident.id).exists():
            raise ValidationError("O residente não pertence ao local especificado.")

        serializer.save()

    def perform_update(self, serializer):
        resident = serializer.validated_data['resident']
        place = serializer.validated_data['place']

        if not place.residents.filter(id=resident.id).exists():
            raise ValidationError("O residente não pertence ao local especificado.")

        serializer.save()
    
class InvoicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoicesSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Invoice.objects.filter(Q(is_active=True) & Q(relation__resident=user)).distinct()
