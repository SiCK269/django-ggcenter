from django.contrib import admin
from django.urls import path, include
from devices.api import app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('devices.urls')),
    path('admin/', admin.site.urls),
    path('api/', app.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)