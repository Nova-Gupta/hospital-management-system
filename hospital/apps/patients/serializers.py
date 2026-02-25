from rest_framework import serializers
from .models import Patient
from hospital.apps.accounts.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'user', 'date_of_birth', 'blood_group',
                  'address', 'emergency_contact', 'medical_history', 'created_at')

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('date_of_birth', 'blood_group', 'address',
                  'emergency_contact', 'medical_history')