from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvoicesViewSet, RelationInvoiceViewSet

router_relation = DefaultRouter()
router_relation.register(r"relation-invoices", RelationInvoiceViewSet)
router_invoices = DefaultRouter()
router_invoices.register(r"invoices", InvoicesViewSet)

urlpatterns = [
    path("", include(router_relation.urls)),
    path("", include(router_invoices.urls)),
]
