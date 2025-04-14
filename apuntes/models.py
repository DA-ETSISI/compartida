"""
Modelos de la db de la app apuntes.
"""
from django.db import models
from django.contrib.auth.models import User

class Asignatura(models.Model):
    """
    Modelo para almacenar asignaturas.

    atributos:
    - nombre: Nombre de la asignatura.
    - creditos: Número de créditos de la asignatura.

    """
    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField()

class Titulacion(models.Model):
    """
    Modelo para almacenar titulación.

    atributos:
    - nombre: Nombre de la carrera.

    """
    nombre = models.CharField(max_length=255)

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
    pdfdir = models.FileField(upload_to='apuntes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey('apuntes.Asignatura', on_delete=models.SET_NULL, null=True)
    descargas = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apoyo_docente = models.ManyToManyField('usrs.Profesor')
