from rest_framework import serializers
from .models import Doctor
from hospital.apps.accounts.serializers import UserSerializer

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ('id', 'user', 'specialization', 'license_number',
                  'experience_years', 'consultation_fee', 'is_available', 'created_at')

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('specialization', 'license_number', 'experience_years',
                  'consultation_fee', 'is_available')