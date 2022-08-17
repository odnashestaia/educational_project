from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mysite import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('demo.urls')),
    path('api/', include('api.urls')),
]
urlpatterns += static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
