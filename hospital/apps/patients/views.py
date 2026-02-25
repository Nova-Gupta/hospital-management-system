from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer, PatientUpdateSerializer
from hospital.apps.accounts.permissions import IsAdmin, IsAdminOrDoctor

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PatientUpdateSerializer
        return PatientSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrDoctor()]
        if self.action in ['update', 'partial_update', 'me']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            patient = request.user.patient_profile
        except Patient.DoesNotExist:
            return Response({'error': 'Patient profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = PatientSerializer(patient)
        else:
            serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)