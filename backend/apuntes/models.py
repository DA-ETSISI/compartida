"""
This module defines two Django models: Apunte and ejercicios.

Models:
    Apunte: Represents a study note or document uploaded by a user. It includes attributes 
        such as title, file path, creation date, associated subject, download count, uploader, 
        associated professors, and a description.

    ejercicios: Represents an exercise with attributes such as statement, optional PDF file, 
        creation date, associated subject, associated topic, view count, and uploader.
"""
from django.db import models
from usrs.models import Asignatura, UsrDa, Profesor


class Titulacion(models.Model):
    """
    Represents an academic degree or program.

    Attributes:
        nombre (CharFiled): The name of the degree.
        codigo (CharField): A unique code for the degree, limited to 10 characters.
    """

    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=10, default="", unique=True)
    tipo = models.CharField(max_length=10, default="GRA", blank=True)

class Asignatura(models.Model):
    """
    Model representing an academic subject.

    Attributes:
        nombre (CharField): The name of the subject, with a maximum length of 255 characters.
        creditos (IntegerField): The number of credits assigned to the subject.
        curso (IntegerField): The course number in which the subject is taught.
        optativa (BooleanField): Indicates whether the subject is optional (True) or mandatory (
            False). Defaults to False.
        grados (ManyToManyField): A many-to-many relationship with the Titulacion model, 
            representing the degrees associated with the subject. This field is required.
    """
    codigo = models.CharField(max_length=20, primary_key=True, unique=True, default="")

    nombre = models.CharField(max_length=255)
    creditos = models.IntegerField(default=6)
    curso = models.IntegerField(default=0)
    optativa = models.BooleanField(default=False)

    grados =  models.ManyToManyField('Titulacion', symmetrical=False, blank=False)

class Apunte(models.Model):
    """
    Apunte Model

    Represents a study note or document uploaded by a user.

    Attributes:
        titulo (CharField): The title of the note, limited to 255 characters.
        pdfdir (FileField): The file path to the uploaded PDF document.
        fecha_creacion (datetime): The timestamp when the note was created. 
            Automatically set on creation.
        asignatura (ForeignKey): A foreign key to the Asignatura model, representing the 
            subject associated with the note. Can be null if not assigned to a subject.
        user (ForeignKey): A foreign key to the UsrDa model, representing the user who 
            uploaded the note.
        apoyo_docente (ManyToManyField): A many-to-many relationship with the Profesor model,
            representing the professors who support or are associated with the note.
        descripcion (CharField): A textual description of the note. Defaults to an empty string.
        visualizaciones (IntegerField): The number of times the note has been viewed. Defaults to 0.
        visible (BooleanField): A flag indicating whether the note is visible to users. 
            Defaults to True.
    """

    titulo = models.CharField(max_length=255)
    pdfdir = models.FileField(upload_to='apuntes/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UsrDa, on_delete=models.CASCADE)
    apoyo_docente = models.ManyToManyField(Profesor)
    descripcion = models.TextField(default="")
    visualizaciones = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)

class Ejercicios(models.Model):
    """
    Model representing an exercise (ejercicio).

    Attributes:
        enunciado (TextField): The statement or description of the exercise.
        fecha_creacion (DateTimeField): The timestamp when the exercise was created.
            Automatically set to the current date and time when created.
        asignatura (ForeignKey): A foreign key linking the exercise to an Asignatura instance.
            Allows null values and sets the field to NULL if the related Asignatura is deleted.
        visualizaciones (IntegerField): The number of times the exercise has been viewed.
            Defaults to 0.
        visible (BooleanField): A flag indicating whether the exercise is visible to users.
            Defaults to True.
        user (ForeignKey): A foreign key linking the exercise to a UsrDa instance.
            Deleting the related UsrDa will also delete the exercise.
    """

    enunciado = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    visualizaciones = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    user = models.ForeignKey(UsrDa, on_delete=models.CASCADE)
