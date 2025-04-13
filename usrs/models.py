"""
Modelos de la app usrs.
"""
from django.contrib.auth.models import User
from django.db import models
from apuntes.models import Titulacion, Asignatura

class UsrDa(models.Model):
    """
    Modelo de usuario personalizado que hereda de AbstractUser => django.user + usrs.user.
    Se pueden añadir campos adicionales si es necesario.
    atributos:
    - Titulación (titulacion_id): Relación con el modelo titulación.
    - Recuento de subidas (int): Número de apuntes subidos por el usuario.
    - Recuento de descargas (int): Número de apuntes descargados por el usuario.
    - Es profesor (Bool): Booleano que indica si el usuario es profesor o no.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    titulacion = models.ForeignKey(Titulacion, on_delete=models.SET_NULL)
    recuento_subidas = models.IntegerField(default=0)
    recuento_descargas = models.IntegerField(default=0)
    es_profesor = models.BooleanField(default=False)

class Profesor(models.Model):
    """
    Modelo para almacenar profesores.
    atributos:
    - user (user_id => int): Usuario que subió el apunte => enlace a la tabla user, Si se borra el
        usuario se borran los apuntes.
    - asignaturas (asignatura_id => int): Asignaturas impartidas por el profesor => enlace a la
        tabla asignatura, Si se borra la asignatura se pone a null.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(Asignatura, on_delete=models.SET_NULL, blank=True)
