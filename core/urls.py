from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/token/login/', obtain_auth_token, name='api_token_auth'),
    path('auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('apps.user.urls')),

    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)