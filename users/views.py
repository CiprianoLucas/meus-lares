from django.shortcuts import render
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.http import JsonResponse

@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})   