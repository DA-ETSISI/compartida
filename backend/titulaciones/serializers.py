from rest_framework import serializers
from .models import Titulacion, Asignatura

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = "__all__"

class AsignaturaGradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = ["grados"]

class TitulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titulacion
        fields = "__all__"