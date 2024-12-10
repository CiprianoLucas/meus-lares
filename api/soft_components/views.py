from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


class SoftPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"


class SoftModelsViewSet(viewsets.ModelViewSet):
    pagination_class = SoftPagination
    permission_classes = [IsAuthenticated]
    request: Request
