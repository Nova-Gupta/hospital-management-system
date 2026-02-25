from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Invoice
from .serializers import InvoiceSerializer
from hospital.apps.accounts.permissions import IsAdmin

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Invoice.objects.select_related('appointment').all()
        elif user.is_doctor():
            return Invoice.objects.select_related('appointment').filter(
                appointment__doctor=user.doctor_profile)
        else:
            return Invoice.objects.select_related('appointment').filter(
                appointment__patient=user.patient_profile)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'mark_paid']:
            return [IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAdmin()]
        return [IsAdmin()]

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def mark_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.payment_status = Invoice.PaymentStatus.PAID
        invoice.payment_method = request.data.get('payment_method', Invoice.PaymentMethod.CASH)
        invoice.paid_at = timezone.now()
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)