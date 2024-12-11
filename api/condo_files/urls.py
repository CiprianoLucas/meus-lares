from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AptInspectImagesView, ContractsFilesView

router = DefaultRouter()
router.register(r"inspect", AptInspectImagesView, "file-inspect")
router.register(r"contract", ContractsFilesView, "file-contract")

urlpatterns = [path("", include(router.urls))]
