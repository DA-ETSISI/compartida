from rest_framework import serializers

from usrs.models import UsrDa, Profesor, Asignatura, Titulacion

class GenericUserDASerializer(serializers.ModelSerializer):    
    class Meta:
        model = UsrDa
        fields = [
                    'id',
                    'preferred_username',
                    'email',
                    'name',
                    'es_profesor',
                    'is_staff',
                    'is_active',
                    'titulacion'
                ]

class StaffUserDASerializer(serializers.ModelSerializer):
    class Meta:
        model = UsrDa
        fields = ['is_staff']


class ActiveUserDASerializer(serializers.ModelSerializer):
    class Meta:
        model = UsrDa
        fields = ['is_active']
