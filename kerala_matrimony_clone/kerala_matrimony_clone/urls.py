
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('built_in_admin/', admin.site.urls),
    path('',include('auth_app.urls')),
    path('admin/',include('admin_app.urls'))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)