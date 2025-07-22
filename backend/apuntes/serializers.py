from rest_framework import serializers
from .models import Apunte

class LoadApunteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        exclude = ['apoyo_docente', 'visualizaciones', 'visible']

class GetApunteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        fields = '__all__'

class ListApunteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apunte
        fields = ['id', 'titulo', 'fecha_creacion', 'user', 'visualizaciones', 'apoyo_docente', 'visible']