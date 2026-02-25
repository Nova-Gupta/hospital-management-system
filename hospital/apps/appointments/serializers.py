from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'doctor', 'doctor_name', 'patient', 'patient_name',
                  'appointment_date', 'appointment_time', 'status', 'reason', 'notes',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        date = attrs.get('appointment_date')
        time = attrs.get('appointment_time')
        qs = Appointment.objects.filter(doctor=doctor, appointment_date=date, appointment_time=time)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This doctor already has an appointment at this time.")
        return attrs