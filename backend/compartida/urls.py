from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('apuntes/', include('apuntes.urls')),
    #path('usrs/', include('usrs.urls')),
    path('usr/login/', include('mozilla_django_oidc.urls')),
    # Swagger, auth, etc.
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]