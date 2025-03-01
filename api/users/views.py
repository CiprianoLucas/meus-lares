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
from relations.models import CondoStaff, CondoTenant
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView
from soft_components.views import SoftModelsViewSet

from .models import User
from .serializers import CustomSignupSerializer, UserSerializer


@api_view(["GET"])
def get_info(request: HttpRequest):
    csrftoken = get_token(request)
    response = {
        "csrftoken": csrftoken,
        "id": request.user.id if not request.user.is_anonymous else "",
        "nick": request.user.nick if not request.user.is_anonymous else "",
    }
    return JsonResponse(response)


class FindUserByEmailView(APIView):

    def get(self, _, email: str):

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        name_split = user.full_name.split(" ")

        response = {
            "name": name_split[0] + " " + name_split[1][0:2] + "...",
            "id": user.id,
        }
        return JsonResponse(response)


class UserProfileView(SoftModelsViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        users = User.objects.filter(id=user.id).distinct()
        return users


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
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return JsonResponse(
                {"error": "Email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)
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
                    {"error": """Verifique seu e-mail."""},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            perform_login(request, user, email_verification=None)
            roles = list(CondoStaff.objects.filter(user=user).values("role"))
            roles = list(set([role["role"] for role in roles]))
            if CondoTenant.objects.filter(user=user).exists():
                roles.append("tenant")

            response = {"nick": user.nick, "roles": roles, "id": user.id}

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
                response = {"has_user": False, "email": email, "full_name": name}

                return JsonResponse(response, status=status.HTTP_200_OK)

            perform_login(request, user, email_verification=None)
            roles = list(CondoStaff.objects.filter(user=user).values("role"))
            roles = list(set([role["role"] for role in roles]))
            if CondoTenant.objects.filter(user=user).exists():
                roles.append("tenant")

            response = {
                "has_user": True,
                "nick": user.nick,
                "roles": roles,
                "email": user.email,
                "id": user.id,
            }

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


def roles_view(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse(
            {"error": "Usuário não está logado"},
            status=status.HTTP_403_FORBIDDEN,
        )

    roles = list(CondoStaff.objects.filter(user=user).values("role"))
    roles = list(set([role["role"] for role in roles]))
    if CondoTenant.objects.filter(user=user).exists():
        roles.append("tenant")

    return JsonResponse({"roles": roles}, status=status.HTTP_200_OK)


def logout_view(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)

    return HttpResponse(status=204)
