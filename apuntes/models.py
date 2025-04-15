"""
Modelos de la db de la app apuntes.
"""
from django.db import models
from usrs.models import Asignatura, UsrDa, Profesor

class Apunte(models.Model):
    """
    Modelo para almacenar apuntes.

    atributos:
    - titulo (str): Título del apunte.
    - pdfdir (dir => str): dirección de el pdf de los apuntes (apuntes/).
    - fecha_creacion (dateTime): Fecha de creación del apunte.
    - asignatura (asignatura_id => int): Asignatura a la que pertenece el apunte => enlace a la 
        tabla asignatura, Si se borra el modelo de referencia se pone a null.
    - descargas (int): Número de descargas del apunte.
    - user (user_id => int): Usuario que subió el apunte => enlace a la tabla user, Si se borra el
        usuario se borran los apuntes.
    - apoyo_docente (user_id => int): Usuario que subió el apunte => enlace a la tabla user, Si se
        borra el usuario se borran los apuntes.
    """
    titulo = models.CharField(max_length=255)
    pdfdir = models.FileField(upload_to='uploads/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    descargas = models.IntegerField(default=0)
    user = models.ForeignKey(UsrDa, on_delete=models.CASCADE)
    apoyo_docente = models.ManyToManyField(Profesor)
    descipcion = models.TextField(default="")
