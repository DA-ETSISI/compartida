from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('apuntes/', include('apuntes.urls')),
    path('usrs/', include('usrs.urls')),
    # Swagger, auth, etc.
]