from soft_components.views import SoftModelsViewSet
from rest_framework.decorators import api_view
from .models import RecurringFee, BreachPenalty, FinePenalty
from .serializers import RecurringFeeSerializer, BreachPenaltySerializer, FinePenaltySerializer
from django.db.models import Q


class BreachPenaltyView(SoftModelsViewSet):
    serializer_class = BreachPenaltySerializer

    def get_queryset(self):
        user = self.request.user

        user_penalities = BreachPenalty.objects.filter(
            Q(contract__related_object__user=user) |
            Q(contract__related_object__apartment__condominium__condostaff__user=user,
            contract__related_object__apartment__condominium__condostaff__role__in=["owner"])
        ).distinct()

        return user_penalities


class RecurringFeeView(SoftModelsViewSet):
    serializer_class = RecurringFeeSerializer

    def get_queryset(self):
        user = self.request.user

        user_bills = RecurringFee.objects.filter(
            Q(contract__related_object__user=user) |
            Q(contract__related_object__apartment__condominium__condostaff__user=user,
            contract__related_object__apartment__condominium__condostaff__role__in=["owner"])
        ).distinct()

        return user_bills
    
class FinePenaltyView(SoftModelsViewSet):
    serializer_class = FinePenaltySerializer

    def get_queryset(self):
        user = self.request.user

        user_fines = FinePenalty.objects.filter(
            Q(contract__related_object__user=user) |
            Q(contract__related_object__apartment__condominium__condostaff__user=user,
            contract__related_object__apartment__condominium__condostaff__role__in=["owner"])
        ).distinct()

        return user_fines

@api_view(["POST"])
def calculate_penality(request):
    pass
    
    
    
    
    
        
    
    
    