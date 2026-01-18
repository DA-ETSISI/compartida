from rest_framework.routers import DefaultRouter

from .views import ApunteCreateViewSet, ApunteListViewSet, ApunteRetrieveViewSet

router = DefaultRouter()
router.register(r"load", ApunteCreateViewSet, basename="subir-apuntes")
router.register(r"apunte", ApunteRetrieveViewSet, basename="get-apuntes")
router.register(r"list", ApunteListViewSet, basename="list-apuntes")


urlpatterns = router.urls
