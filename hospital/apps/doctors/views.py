from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer, DoctorUpdateSerializer
from hospital.apps.accounts.permissions import IsAdmin, IsAdminOrDoctor

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return DoctorUpdateSerializer
        return DoctorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'me', 'available']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def available(self, request):
        doctors = Doctor.objects.filter(is_available=True).select_related('user')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            doctor = request.user.doctor_profile
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = DoctorSerializer(doctor)
        else:
            serializer = DoctorUpdateSerializer(doctor, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)