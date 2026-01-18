from rest_framework.routers import DefaultRouter

from .views import CurrentUserViewSet, UserDAListViewSet, UserDARetrieveViewSet

router = DefaultRouter()
router.register(r"admin/list", UserDAListViewSet, basename="list-users")
router.register(r"admin/get", UserDARetrieveViewSet, basename="get-user")
router.register(r"", CurrentUserViewSet, basename="current-user-info")


urlpatterns = router.urls
