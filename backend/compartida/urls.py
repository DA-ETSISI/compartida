from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import IsAdminUser

urlpatterns = [
    path("apuntes/", include("apuntes.urls")),
    path("usrs/", include("usrs.urls")),
    path("titulaciones/", include("titulaciones.urls")),
    # Siu login
    path("usrs/login/", include("mozilla_django_oidc.urls")),
    # Swagger, auth, etc.
    path(
        "schema/",
        SpectacularAPIView.as_view(permission_classes=[IsAdminUser]),
        name="schema",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema", permission_classes=[IsAdminUser]
        ),
        name="swagger-ui",
    ),
]
