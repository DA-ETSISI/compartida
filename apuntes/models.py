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
from usrs.models import Asignatura, UsrDa, Profesor, Tema

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
        descargas (IntegerField): The number of times the note has been downloaded. Defaults to 0.
        user (ForeignKey): A foreign key to the UsrDa model, representing the user who 
            uploaded the note.
        apoyo_docente (ManyToManyField): A many-to-many relationship with the Profesor model,
            representing the professors who support or are associated with the note.
        descripcion (CharField): A textual description of the note. Defaults to an empty string.
        visualizaciones (IntegerField): The number of times the note has been viewed. Each user 
            counts only once towards the view count. Defaults to 0.
    """

    titulo = models.CharField(max_length=255)
    pdfdir = models.FileField(upload_to='uploads/apuntes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    descargas = models.IntegerField(default=0)
    user = models.ForeignKey(UsrDa, on_delete=models.CASCADE)
    apoyo_docente = models.ManyToManyField(Profesor)
    descripcion = models.TextField(default="")
    visualizaciones = models.IntegerField(default=0)

class Ejercicios(models.Model):
    """
    Model representing an exercise (ejercicio).

    Attributes:
        enunciado (TextField): The statement or description of the exercise.
        pdfdir (FileField): Optional file field to upload a PDF related to the exercise.
            Files are uploaded to the 'uploads/ejercicios' directory.
        fecha_creacion (DateTimeField): The timestamp when the exercise was created.
            Automatically set to the current date and time when created.
        asignatura (ForeignKey): A foreign key linking the exercise to an Asignatura instance.
            Allows null values and sets the field to NULL if the related Asignatura is deleted.
        tema (ForeignKey): A foreign key linking the exercise to a Tema instance.
            Allows null values and sets the field to NULL if the related Tema is deleted.
        visualizaciones (IntegerField): The number of times the exercise has been viewed.
            Defaults to 0.
        user (ForeignKey): A foreign key linking the exercise to a UsrDa instance.
            Deleting the related UsrDa will also delete the exercise.
    """

    enunciado = models.TextField()
    pdfdir = models.FileField(upload_to='uploads/ejercicios', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.SET_NULL, null=True)
    tema =  models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    visualizaciones = models.IntegerField(default=0)
    user = models.ForeignKey(UsrDa, on_delete=models.CASCADE)
