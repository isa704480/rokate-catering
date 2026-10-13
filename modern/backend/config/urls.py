from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

admin.site.site_header = "Rokate Catering"
admin.site.site_title = "Rokate — админ"
admin.site.index_title = "Панель управления"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/", include("apps.core.api_urls")),
    path("api/panel/", include("apps.panel.urls")),
    path("healthz", lambda r: JsonResponse({"ok": True})),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
