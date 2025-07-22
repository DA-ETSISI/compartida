from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'admin/list', UserDAListViewSet, basename='list-users')
router.register(r'admin/get', UserDARetrieveViewSet, basename='get-user')


urlpatterns = router.urls