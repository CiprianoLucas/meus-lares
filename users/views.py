from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from .models import User
from places.models import Places
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

@api_view(['GET'])
def get_info(request):
    get_token(request)
    user = request.user
    is_resident = Places.objects.filter(Q(is_active=True) & Q(residents=user)).exists()
    is_union = Places.objects.filter(Q(is_active=True) & (Q(unions=user) | Q(representative=user))).exists()
    
    response = {
        'username': user.username,
        'isResident' : is_resident,
        'isUnion' : is_union,
    }
    print(response)
    
    return JsonResponse(response)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))
        
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            is_resident = Places.objects.filter(Q(is_active=True) & Q(residents=user)).exists()
            is_union = Places.objects.filter(Q(is_active=True) & (Q(unions=user) | Q(representative=user))).exists()
            response = {
                'username': user.username,
                'isResident' : is_resident,
                'isUnion' : is_union
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return HttpResponse(status=204)