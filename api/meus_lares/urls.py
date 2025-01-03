from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls")),
    path("account/", include("allauth.urls")),
    path("place/", include("places.urls")),
    path("relation/", include("relations.urls")),
    path("file/", include("condo_files.urls")),
    path("bill/", include("bills.urls")),
    path("notification/", include("notifications.urls")),
    # path('request/', include('requests.urls')),
    # path('invoice/', include('invoices.urls')),
    # path('ai/', include('ai.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
