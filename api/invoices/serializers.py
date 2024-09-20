from rest_framework import serializers
from .models import RelationInvoice, Invoice

class RelationInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationInvoice
        fields = '__all__'
        
class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
