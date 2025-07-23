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
    staff_serializer_class = StaffUserDASerializer
    active_serializer_class = ActiveUserDASerializer

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

    def get_serializer_class(self):
        if self.action == 'set_staff':
            return self.staff_serializer_class
        elif self.action == 'set_active':
            return self.active_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=["patch"], url_path="staff")
    @extend_schema(
        responses={200: StaffUserDASerializer},
        description="Cambiar la visibilidad de un apunte"
    )
    def set_staff(self, request, id = None):
        if not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        userda = self.get_object()
        serializer = self.get_serializer(userda, data = request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["patch"], url_path="active")
    @extend_schema(
        responses={200: StaffUserDASerializer},
        description="Cambiar la visibilidad de un apunte"
    )
    def set_active(self, request, id = None):
        if not request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        userda = self.get_object()
        serializer = self.get_serializer(userda, data = request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

