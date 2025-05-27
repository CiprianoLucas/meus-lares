from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from .permissions import SoftModelsPermission
from .models import SoftModel


class SoftPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = "page_size"


class SoftModelsViewSet(viewsets.ModelViewSet):
    pagination_class = SoftPagination
    # permission_classes = [SoftModelsPermission]
    search: list = []
    sort: dict = {}
    request: Request
    get_role: list[str] = ["*"]
    update_role: list[str] = ["owner"]
    create_role: list[str] = ["owner"]
    delete_role: list[str] = []

    def filter_by_roles(self, cls: SoftModel, user=None, roles=None):
        if not user:
            user = self.request.user
        if not roles:
            roles = self.get_role

        cls.filter_by_roles(user, roles)

    def perform_destroy(self, instance):
        instance.delete(user=self.request.user)

    def search_sort(self, query):

        query_params = self.request.query_params
        search = query_params.get("search")
        sort_by = query_params.get("sort_by")
        sort_asc = query_params.get("sort_asc")

        if search:
            queryset = Q()
            for param in self.search:
                queryset |= Q(**{param: search})

            query = query.filter(queryset)

        if sort_by and sort_by in self.sort.keys():
            sort_prefix = "" if sort_asc == "true" else "-"
            sort_field = sort_prefix + self.sort[sort_by]
            query = query.order_by(sort_field)

        else:
            query = query.order_by("-created_at")

        return query
