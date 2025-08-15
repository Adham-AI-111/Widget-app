from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('admin-urls/', include('custom_admin.urls')),
]

if settings.DEBUG:  # ✅ only in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)