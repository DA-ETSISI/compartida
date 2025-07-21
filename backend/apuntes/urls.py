"""
Django REST api urls for the 'apuntes' app.
This module defines the URL patterns for the 'apuntes' app, which handles study notes and exercises.
It includes routes for listing, creating, retrieving, updating, and deleting study notes (apuntes) and exercises.
"""

from rest_framework.routers import DefaultRouter
from .views import ApunteViewSet

router = DefaultRouter()
router.register(r'load', ApunteViewSet, basename='apuntes')

urlpatterns = router.urls
