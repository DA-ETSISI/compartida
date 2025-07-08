"""
URL configuration for compartida project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("upload/", views.subir_apunte),
    path("apuntes/", views.lista_apuntes),
    path("apuntes/visualizador/<int:apunte_id>/", views.visualizador_apuntes),
    path("apuntes/delete/<int:apunte_id>/", views.eliminar_apunte),
    path("apuntes/apoyo_docente/<int:apunte_id>/", views.apoyo_docente),
    path("staff/asignaturas/crear/", views.crear_asignatura),
    path("staff/asignaturas/lista/", views.lista_asignaturas),
    path("staff/asignaturas/delete/<int:asignatura_id>/", views.delete_asignatura),
    path("staff/asignaturas/edit/<int:asignatura_id>/", views.editar_asignatura),
    path("staff/titulacion/crear/", views.crear_titulacion),
    path("staff/titulacion/lista/", views.lista_titulacion),
    path("staff/titulacion/delete/<int:titulacion_id>/", views.delete_titulacion),
    path("staff/titulacion/edit/<int:titulacion_id>/", views.editar_titulcion),
    path("staff/apuntes_aprobar/", views.aprobar_apuntes),
    path("staff/apuntes_aprobar/<int:apunte_id>/", views.aprobado),

]
