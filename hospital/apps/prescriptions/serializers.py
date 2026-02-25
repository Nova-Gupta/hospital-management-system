from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ('id', 'appointment', 'diagnosis', 'medications',
                  'instructions', 'follow_up_date', 'created_at')
        read_only_fields = ('created_at',)