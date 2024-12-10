import time

from allauth.account.models import EmailAddress
from allauth.account.utils import perform_login
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest
from django.middleware.csrf import get_token
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import User
from .serializers import CustomSignupSerializer


@api_view(["GET"])
def get_info(request: HttpRequest):
    csrftoken = get_token(request)
    user = request.user

    response = {"username": user.username, "csrftoken": csrftoken}

    return JsonResponse(response)


class UserCreateView(generics.CreateAPIView):
    serializer_class = CustomSignupSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"detail": "Usuário registrado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request: Request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return JsonResponse(
                    {
                        "error": """Sua conta foi desativada.
                        Entre em contato com nosso suporte."""
                    },
                    status=status.HTTP_410_GONE,
                )

            email_address = EmailAddress.objects.filter(user=user, primary=True).first()
            if not email_address or not email_address.verified:
                email_address.send_confirmation(request)
                return JsonResponse(
                    {
                        "error": """Seu e-mail ainda não foi verificado.
                        Verifique sua caixa de entrada do e-mail."""
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            perform_login(request, user, email_verification=None)

            response = {"email": user.email}
            return JsonResponse(response)

        return JsonResponse(
            {"error": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED
        )


class GoogleLogin(APIView):

    def post(self, request: Request, *args, **kwargs):
        token = request.data.get("access_token")

        if not token:
            return JsonResponse(
                {"error": "Access token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            if idinfo["aud"] != settings.GOOGLE_CLIENT_ID:
                return JsonResponse(
                    {"error": "Invalid audience."}, status=status.HTTP_401_UNAUTHORIZED
                )

            if idinfo.get("exp") < int(time.time()):
                return JsonResponse(
                    {"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED
                )

            email = idinfo.get("email")
            name = idinfo.get("name")

            user = User.objects.filter(email=email).first()

            if not user:
                response = {
                    "has_user": False,
                    "email": email,
                    "full_name": name,
                    "email": email,
                }

                return JsonResponse(response, status=status.HTTP_200_OK)

            perform_login(request, user, email_verification=None)

            response = {"has_user": True}

            return JsonResponse(response, status=status.HTTP_200_OK)

        except ValueError:
            return JsonResponse(
                {"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception:
            return JsonResponse(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)

    return HttpResponse(status=204)
