from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from .models import User

@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))
