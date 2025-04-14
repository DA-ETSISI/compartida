"""
apuntes/views.py
Views for the apuntes app.
"""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from usrs.models import UsrDa
from .models import Apunte


# Create your views here.
def index(request):
    """
    Index view for the apuntes app.
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

@login_required(login_url="/usr/login/")  # Redirect to login page if not authenticated
def subir_apunte(request):
    """
    View for uploading apuntes.
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
