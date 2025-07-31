from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status
from django.http import Http404
