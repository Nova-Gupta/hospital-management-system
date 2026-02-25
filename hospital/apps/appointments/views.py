from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from hospital.apps.accounts.permissions import IsAdmin, IsAdminOrDoctor

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Appointment.objects.select_related('doctor__user', 'patient__user').all()
        elif user.is_doctor():
            return Appointment.objects.select_related('doctor__user', 'patient__user').filter(
                doctor=user.doctor_profile)
        else:
            return Appointment.objects.select_related('doctor__user', 'patient__user').filter(
                patient=user.patient_profile)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'update_status']:
            return [IsAuthenticated()]
        return [IsAdmin()]

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminOrDoctor])
    def update_status(self, request, pk=None):
        appointment = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Appointment.Status.choices):
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)
        appointment.status = new_status
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)