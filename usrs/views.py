"""
Module: usrs.views
This module contains views for user authentication and management.
It includes a logout view that allows users to log out of the application.
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader

from .models import UsrDa

# Create your views here.
@login_required
def logout(request):
    """
    Logout the user and redirect to the home page.
    This view is protected by the login_required decorator, which means
    that only authenticated users can access it. If a user is not authenticated,
    they will be redirected to the login page.
    The view uses the request.user.logout() method to log out the user,
    and then redirects them to the home page.

    Args:
        request (HttpRequest): The HTTP request object containing the session data.

    Returns:
        HttpResponseRedirect: A redirect to the home page after logging out.
    """

    request.session.flush()  # Clear the session data

    return redirect('/')


@user_passes_test(lambda u: u.is_staff)
def lista_usuarios(request):
    """
    View to list all users in the system.
    This view is protected by the user_passes_test decorator, which means
    that only users with staff status can access it. If a user does not have
    staff status, they will be redirected to the login page.

    Args:
        request (HttpRequest): The HTTP request object containing the session data.

    Returns:
        HttpResponse: A response containing the list of users.
    """
    doc_template = loader.get_template('staff/lista_users.html')

    ctx = {
        'user': UsrDa.objects.get(id=request.user.id),
        'usuarios': UsrDa.objects.all(),
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)

@user_passes_test(lambda u: u.is_staff)
def editat_usuario(request, user_id):
    """
    View to edit a user in the system.
    This view is protected by the user_passes_test decorator, which meansx
    that only users with staff status can access it. If a user does not have 
    staff status, they will be redirected to the login page.

    Args:
        request (HttpRequest): The HTTP request object containing the session data.
        id (int): The ID of the user to be edited.

    Returns:
        HttpResponse: A response containing the edit user form.
    """
    doc_template = loader.get_template('usrs/editar_users.html')

    ctx = {
        'title': 'Edita Usuario',
        'usuario': UsrDa.objects.get(id=user_id),
    }

    doc = doc_template.render(ctx, request)

    return HttpResponse(doc)
