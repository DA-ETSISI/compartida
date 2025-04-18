"""
Module: usrs.views
This module contains views for user authentication and management.
It includes a logout view that allows users to log out of the application.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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
    """

    request.session.flush()  # Clear the session data

    return redirect('/')
