from rest_framework.routers import DefaultRouter

from .views import (
    AsignaturaListViewSet,
    AsignaturaRetrieveViewSet,
    TitulacionListViewSet,
)

router = DefaultRouter()

router.register(r"asignatura", AsignaturaRetrieveViewSet, basename="get-asignatura")
router.register(r"asignaturas", AsignaturaListViewSet, basename="get-asignaturas")
router.register(r"", TitulacionListViewSet, basename="get-titulacion")

urlpatterns = router.urls
