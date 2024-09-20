from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RelationInvoiceViewSet, InvoicesViewSet

router_relation = DefaultRouter()
router_relation.register(r'relation-invoices', RelationInvoiceViewSet)
router_invoices = DefaultRouter()
router_invoices.register(r'invoices', InvoicesViewSet)

urlpatterns = [
    path('', include(router_relation.urls)),
    path('', include(router_invoices.urls)),
]
