from rest_framework import serializers
from .models import RelationInvoice, Invoice

class RelationInvoiceSerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()
    resident_name = serializers.SerializerMethodField()
    class Meta:
        model = RelationInvoice
        fields = ["id", "company", "unit_number", "resident", "place", "resident_name", "place_name"]
        extra_kwargs = {
            "status": {"read_only": True},
            "resident_name": {"read_only": True},
            "place_name": {"read_only": True},
        }
    
    def get_place_name(self, obj):
        if obj.place:
            return obj.place.name
        return None
    
    def get_resident_name(self, obj):
        if obj.resident:
            return obj.resident.username
        return None
        
class InvoicesSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ["id", "value", "ticket_number", "company"]
        
    def get_company(self, obj):
        if obj.relation:
            return obj.relation.company
        return None