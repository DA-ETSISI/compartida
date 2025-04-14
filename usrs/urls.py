"""
URL configuration for compartida project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from mozilla_django_oidc import views as oidc_views

urlpatterns = [
    path('login/', oidc_views.OIDCAuthenticationRequestView.as_view(), name='oidc_authentication_init'),
    path('login/callback/', oidc_views.OIDCAuthenticationCallbackView.as_view(), name='oidc_authentication_callback'),
    path('logout/', oidc_views.OIDCLogoutView.as_view(), name='oidc_logout'),
]