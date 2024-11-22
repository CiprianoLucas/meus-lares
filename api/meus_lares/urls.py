from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    # path('place/', include('places.urls')),
    # path('request/', include('requests.urls')),
    # path('invoice/', include('invoices.urls')),
    # path('ai/', include('ai.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)