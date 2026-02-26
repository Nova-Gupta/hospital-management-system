from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Prescription
from .serializers import PrescriptionSerializer
from hospital.apps.accounts.permissions import IsAdminOrDoctor

class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            if user.is_admin():
                return Prescription.objects.select_related('appointment').all()
            elif user.is_doctor():
                return Prescription.objects.select_related('appointment').filter(
                    appointment__doctor=user.doctor_profile)
            else:
                return Prescription.objects.select_related('appointment').filter(
                    appointment__patient=user.patient_profile)
        except Exception:
            return Prescription.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrDoctor()]
        return [IsAuthenticated()]