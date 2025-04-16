"""
Module for handling views related to the 'apuntes' app.
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from usrs.models import UsrDa
from .models import Apunte


# Create your views here.
def index(request) -> HttpResponse:
    """
    Handles the rendering of the index page for the "apuntes" application.
    This view retrieves the top 3 "Apunte" objects ordered by the number of downloads,
    as well as the top 3 users with the most uploads and downloads, respectively.
    It then renders the "apuntes/index.html" template with the provided context.
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
    Returns:
        HttpResponse: The rendered HTML document for the index page.
    """

    doc_template = loader.get_template("apuntes/index.html")

    apuntes = Apunte.objects.order_by("descargas")[:3]
    top_subidas = UsrDa.objects.order_by("recuento_subidas")[:3]
    top_descargas = UsrDa.objects.order_by("recuento_descargas")[:3]

    ctx = {
        "user": request.user.is_authenticated,
        "apuntes": apuntes,
        "top_subidas": top_subidas,
        "top_descargas": top_descargas,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@login_required(login_url="/usr/login/")
def subir_apunte(request) -> HttpResponse:
    """
    Handles the upload of a PDF file and saves it as an "Apunte" object.

    This view renders a template for uploading a file and processes the form 
    submission when the request method is POST. It saves the uploaded file 
    along with additional metadata (title, description, and user) to the database.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request and user.

    Returns:
        HttpResponse: The rendered HTML document for the upload page.
    """

    doc_template = loader.get_template("apuntes/subir.html")

    if request.method == "POST":
        # Handle file upload
        uploaded_file = request.FILES["archivo_pdf"]
        apunte = Apunte(
            titulo=request.POST["tema"],
            pdfdir=uploaded_file,
            user=request.user,
            descripcion=request.POST["descripcion"],
        )
        apunte.save()

    ctx = {
        "user": request.user.is_authenticated,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@login_required(login_url="/usr/login/")
def lista_apuntes(request) -> HttpResponse:
    """
    Renders a list of uploaded "Apunte" objects.

    This view retrieves all "Apunte" objects from the database and renders them
    in a template. It also includes a context variable to indicate whether the
    user is authenticated.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.

    Returns:
        HttpResponse: The rendered HTML document for the list of apuntes.
    """

    doc_template = loader.get_template("apuntes/lista.html")

    apuntes = Apunte.objects.all().order_by("visualizaciones", "-fecha_creacion")

    es_staff = request.user.is_staff
    es_profesor = request.user.es_profesor

    ctx = {
        "user": request.user.is_authenticated,
        "apuntes": apuntes,
        "es_staff": es_staff,
        "es_profesor": es_profesor,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)
