from rest_framework import serializers
from .models import Profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=[
            'user',
            'fotografia',
            'telefono',
            'fecha_contratacion',
            'direccion',
            'fecha_nacimiento',
            'numero_identificacion',
            'ubicacion',
            'informacion',
        ]