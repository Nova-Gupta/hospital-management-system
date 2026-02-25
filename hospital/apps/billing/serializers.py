from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'appointment', 'amount', 'tax', 'discount',
                  'total_amount', 'payment_status', 'payment_method', 'paid_at', 'created_at')
        read_only_fields = ('total_amount', 'created_at')