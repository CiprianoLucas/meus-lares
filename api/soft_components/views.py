from django.db.models import Q
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
    search: list = []
    sort: dict = {}
    request: Request
    permission_route : str = None
    permission_get_role : list[str] = ['owner']
    permission_update_role : list[str] = ['owner']
    permission_create_role : list[str] = ['owner']
    permission_delete_role : list[str] = ['owner']

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
