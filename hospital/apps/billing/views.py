from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.select_related('appointment').all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]