from soft_components.serializers import softModelSerializer
from rest_framework import serializers

from .models import RecurringFee, BreachPenalty, FinePenalty


class BreachPenaltySerializer(softModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    
    class Meta:
        model = BreachPenalty
        fields = [
            "id",
            "name",
            "contract",
            "user_fullname",
            "value",
            "is_percentage"
        ]
        extra_kwargs = {"id": {"read_only": True}}
    
    def get_user_fullname(self, obj: BreachPenalty):
        return obj.contract.related_object.user.full_name


class RecurringFeeSerializer(softModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    class Meta:
        model = RecurringFee
        fields = [
            "id",
            "name",
            "contract",
            "user_fullname",
            "break_penalizable",
            "delay_penalizable",
            "value",
            "payment_status",
            "opening_day",
            "due_date"
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user_fullname(self, obj: RecurringFee):
        return obj.contract.related_object.user.full_name
    
    
class FinePenaltySerializer(softModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    class Meta:
        model = FinePenalty
        fields = [
            "id",
            "name",
            "contract",
            "user_fullname",
            "value",
            "status",
            "infraction_type",
            "description"
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user_fullname(self, obj: FinePenalty):
        return obj.contract.related_object.user.full_name 

class CalculatePenalitySerializer(serializers.Serializer):
    contract = serializers.CharField()
    day_left = serializers.DateField()