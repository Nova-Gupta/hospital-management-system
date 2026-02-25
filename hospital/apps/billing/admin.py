from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment', 'total_amount', 'payment_status', 'payment_method', 'paid_at')
    list_filter = ('payment_status', 'payment_method')