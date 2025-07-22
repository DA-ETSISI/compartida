from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions, status

from .serializers import *
from .models import UsrDa

class UserDAListViewSet(ListModelMixin, GenericViewSet):
    permissions_classes = [permissions.IsAuthenticated]
    
    serializer_class = GenericUserDASerializer
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['preferred_username', 'email', 'is_staff']


    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return UsrDa.objects.none()
        return UsrDa.objects.all()


class UserDARetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    permissions_classes = [permissions.IsAuthenticated]
    
    serializer_class = GenericUserDASerializer
    lookup_field = 'id'


    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        if not self.request.user.is_staff:
            return UsrDa.objects.none()
        return UsrDa.objects.all()

