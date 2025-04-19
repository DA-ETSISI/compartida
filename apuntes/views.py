"""
Module for handling views related to the 'apuntes' app.
"""
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.template import loader

from usrs.models import UsrDa, Asignatura, Titulacion
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

    apuntes = Apunte.objects.order_by("visualizaciones")[:3]
    top_subidas = UsrDa.objects.order_by("recuento_subidas")[:3]
    top_descargas = UsrDa.objects.order_by("recuento_visualizaciones")[:3]
    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
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
        asignatura = request.POST["asignatura"]
        asignatura = Asignatura.objects.get(id=asignatura)

        apunte = Apunte(
            titulo=request.POST["tema"],
            pdfdir=uploaded_file,
            user=request.user,
            descripcion=request.POST["descripcion"],
            asignatura=asignatura,
        )
        apunte.save()

    try:
        user = UsrDa.objects.get(id=request.user.id)
        asignaturas = Asignatura.objects.all()
    except UsrDa.DoesNotExist:
        user = None
    except Asignatura.DoesNotExist as error:
        raise Http404("Asignatura not found.") from error

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "asignaturas": asignaturas,
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

    apuntes = Apunte.objects.filter(visible=True).order_by("visualizaciones", "-fecha_creacion")

    es_staff = request.user.is_staff
    es_profesor = request.user.es_profesor

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "es_staff": es_staff,
        "es_profesor": es_profesor,
        "apuntes": apuntes,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def eliminar_apunte(request, apunte_id) -> redirect:
    """
    Handles the deletion of an "Apunte" object.

    This view retrieves the specified "Apunte" object by its ID and deletes it
    from the database. It then redirects the user to the list of apuntes.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        apunte_id (int): The ID of the "Apunte" object to be deleted.

    Returns:
        HttpResponse: A redirect response to the list of apuntes.
    """

    if request.method == "POST":
        try:
            apunte = Apunte.objects.get(id=apunte_id)
            apunte.delete()
        except Apunte.DoesNotExist:
            return Http404("Apunte not found.")

        request.user.recuento_subidas -= 1
        request.user.save()

        return redirect(to="/apuntes/")

@user_passes_test(lambda u: u.es_profesor)
def apoyo_docente(request, apunte_id) -> redirect:
    """
    Assigns the current user (professor) as a supporting staff member for a 
    specific "apunte" (note).
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        apunte_id (int): The ID of the "apunte" (note) to which the supporting staff member 
            will be added.
    Returns:
        HttpResponse: A redirect response to the "/apuntes/" page.
    Raises:
        UsrDa.DoesNotExist: If the user associated with the request does not exist.
        Apunte.DoesNotExist: If the "apunte" with the given ID does not exist.
    """

    if request.method == "POST":
        try:
            pdi = UsrDa.objects.get(id=request.user.id)
            apunte = Apunte.objects.get(id=apunte_id)
        except UsrDa.DoesNotExist:
            return HttpResponseServerError("User not found.")
        except Apunte.DoesNotExist:
            return HttpResponseServerError("Apunte not found.")

        apunte.apoyo_docente.add(pdi)

        return redirect(to="/apuntes/")

@login_required(login_url="/usr/login/")
def visualizador_apuntes(request, apunte_id) -> redirect:
    """
    Handles the display of a specific "Apunte" object.

    This view retrieves the specified "Apunte" object by its ID and increments
    its view count. It then renders a template to display the details of the
    selected "Apunte".

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        apunte_id (int): The ID of the "Apunte" object to be displayed.

    Returns:
        HttpResponse: The rendered HTML document for the selected apunte.
    """

    try:
        apunte = Apunte.objects.get(id=apunte_id)
    except Apunte.DoesNotExist as error:
        raise Http404("Apunte not found.") from error

    if apunte.visible or request.user.is_staff:
        apunte.visualizaciones += 1
        apunte.save()
        request.user.recuento_visualizaciones += 1
        return redirect(to=f"/media/{apunte.pdfdir}")
    else:
        raise Http404("Apunte not found.")

@user_passes_test(lambda u: u.is_staff)
def crear_asignatura(request) -> HttpResponse:
    """
    Handles the creation of a new "Asignatura" object.

    This view renders a template for creating a new "Asignatura" and processes
    the form submission when the request method is POST. It saves the new
    "Asignatura" to the database.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.

    Returns:
        HttpResponse: The rendered HTML document for the create asignatura page.
    """

    doc_template = loader.get_template("staff/crear_asignatura.html")

    if request.method == "POST":

        nombre = request.POST["nombre"]
        creditos = request.POST["creditos"]
        semestre = request.POST["semestre"]

        asignatura = Asignatura(
            nombre=nombre,
            creditos=creditos,
            semestre=semestre,
        )

        asignatura.save()

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def lista_asignaturas(request) -> HttpResponse:
    """
    Renders a list of all "Asignatura" objects.

    This view retrieves all "Asignatura" objects from the database and renders
    them in a template. It also includes a context variable to indicate whether
    the user is authenticated.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.

    Returns:
        HttpResponse: The rendered HTML document for the list of asignaturas.
    """

    doc_template = loader.get_template("staff/lista_asignaturas.html")

    asignaturas = Asignatura.objects.all()

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "is_staff": request.user.is_staff,
        "asignaturas": asignaturas,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def delete_asignatura(request, asignatura_id) -> redirect:
    """
    Handles the deletion of an "Asignatura" object.

    This view retrieves the specified "Asignatura" object by its ID and deletes
    it from the database. It then redirects the user to the list of asignaturas.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        asignatura_id (int): The ID of the "Asignatura" object to be deleted.

    Returns:
        HttpResponse: A redirect response to the list of asignaturas.
    """

    if request.method == "POST":
        try:
            asignatura = Asignatura.objects.get(id=asignatura_id)
            asignatura.delete()
        except Asignatura.DoesNotExist as error:
            raise Http404("Asignatura not found.") from error

        return redirect(to="/staff/asignaturas/lista/")

@user_passes_test(lambda u: u.is_staff)
def editar_asignatura(request, asignatura_id) -> HttpResponse:
    """
    Handles the editing of an existing "Asignatura" object.
    This view retrieves the specified "Asignatura" object by its ID and updates
    its attributes based on the submitted form data. It then redirects the user
    to the list of asignaturas.
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        asignatura_id (int): The ID of the "Asignatura" object to be edited.
    Returns:
        HttpResponse: A redirect response to the list of asignaturas.
    Raises:
        Http404: If the "Asignatura" with the given ID does not exist.
    """

    doc_template = loader.get_template("staff/editar_asignatura.html")

    try:
        asignatura = Asignatura.objects.get(id=asignatura_id)
    except Asignatura.DoesNotExist as error:
        raise Http404("Asignatura not found.") from error

    if request.method == "POST":

        asignatura.nombre = request.POST["nombre"]
        asignatura.creditos = request.POST["creditos"]
        asignatura.save()

        return redirect(to="/staff/asignaturas/lista/")

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "asignatura": asignatura,
    }

    doc = doc_template.render(ctx, request)
    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def crear_titulacion(request) -> HttpResponse:
    """
    Handles the creation of a new "Asignatura" object.

    This view renders a template for creating a new "Asignatura" and processes
    the form submission when the request method is POST. It saves the new
    "Asignatura" to the database.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.

    Returns:
        HttpResponse: The rendered HTML document for the create asignatura page.
    """

    doc_template = loader.get_template("staff/crear_titulacion.html")

    if request.method == "POST":

        nombre = request.POST["nombre"]
        creditos = request.POST["creditos"]

        titulacion = Titulacion(
            nombre=nombre,
            creditos=creditos,
        )

        titulacion.save()

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def lista_titulacion(request) -> HttpResponse:
    """
    Renders a list of all "Asignatura" objects.

    This view retrieves all "Asignatura" objects from the database and renders
    them in a template. It also includes a context variable to indicate whether
    the user is authenticated.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.

    Returns:
        HttpResponse: The rendered HTML document for the list of asignaturas.
    """

    doc_template = loader.get_template("staff/lista_titulacion.html")

    titulaciones = Titulacion.objects.all()

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "titulaciones": titulaciones,
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def delete_titulacion(request, titulacion_id) -> redirect:
    """
    Handles the deletion of an "Asignatura" object.

    This view retrieves the specified "Asignatura" object by its ID and deletes
    it from the database. It then redirects the user to the list of asignaturas.

    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        asignatura_id (int): The ID of the "Asignatura" object to be deleted.

    Returns:
        HttpResponse: A redirect response to the list of asignaturas.
    """

    if request.method == "POST":
        try:
            titulacion = Titulacion.objects.get(id=titulacion_id)
            titulacion.delete()
        except Titulacion.DoesNotExist as error:
            raise Http404("Asignatura not found.") from error

        return redirect(to="/staff/titulacion/lista/")

@user_passes_test(lambda u: u.is_staff)
def editar_titulcion(request, titulacion_id) -> HttpResponse:
    """
    Handles the editing of an existing "Asignatura" object.
    This view retrieves the specified "Asignatura" object by its ID and updates
    its attributes based on the submitted form data. It then redirects the user
    to the list of asignaturas.
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        asignatura_id (int): The ID of the "Asignatura" object to be edited.
    Returns:
        HttpResponse: A redirect response to the list of asignaturas.
    Raises:
        Http404: If the "Asignatura" with the given ID does not exist.
    """

    doc_template = loader.get_template("staff/editar_titulacion.html")

    try:
        titulacion = Titulacion.objects.get(id=titulacion_id)
    except Titulacion.DoesNotExist:
        return Http404("Asignatura not found.")

    if request.method == "POST":

        titulacion.nombre = request.POST["nombre"]
        titulacion.creditos = request.POST["creditos"]

        titulacion.save()

        return redirect(to="/staff/titulacion/lista/")

    try:
        user = UsrDa.objects.get(id=request.user.id)
    except UsrDa.DoesNotExist:
        user = None

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": user,
        "titulacion": titulacion,
    }
    doc = doc_template.render(ctx, request)
    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def aprobar_apuntes(request) -> HttpResponse:
    """
    Handles the approval of "Apunte" objects.
    This view retrieves all "Apunte" objects that are not visible and renders
    them in a template for approval. It also includes a context variable to
    indicate whether the user is authenticated.
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
    Returns:
        HttpResponse: The rendered HTML document for the approval page.
    """
    doc_template = loader.get_template("staff/aprobar_apuntes.html")
    apuntes = Apunte.objects.filter(visible=False).order_by("fecha_creacion")

    ctx = {
        "user": request.user.is_authenticated,
        "user_data": request.user,
        "apuntes": apuntes,
    }
    doc = doc_template.render(ctx, request)
    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def aprobado(request, apunte_id) -> redirect:
    """
    Handles the approval of a specific "Apunte" object.
    This view retrieves the specified "Apunte" object by its ID and sets its
    visibility to True. It then redirects the user to the list of apuntes.
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
            about the request.
        apunte_id (int): The ID of the "Apunte" object to be approved.
    Returns:
        HttpResponse: A redirect response to the list of apuntes.
    """
    if request.method == "POST":
        try:
            apunte = Apunte.objects.get(id=apunte_id)
            apunte.visible = True
            apunte.save()
        except Apunte.DoesNotExist as error:
            raise Http404("Apunte not found.") from error

        return redirect(to="/staff/apuntes_aprobar/")
