from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework import generics
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import status

@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

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
            return JsonResponse({
                'username': user.username,
            })
        else:
            return JsonResponse({'error': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
@csrf_exempt
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    response = JsonResponse({'message': 'Logout realizado com sucesso.'})
    response.delete_cookie('sessionid', path='/')
    return response