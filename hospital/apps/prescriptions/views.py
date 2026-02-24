from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Prescription
from .serializers import PrescriptionSerializer

class PrescriptionViewSet(ModelViewSet):
    queryset = Prescription.objects.select_related('appointment').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]