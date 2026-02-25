from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'blood_group', 'emergency_contact')
    list_filter = ('blood_group',)
    search_fields = ('user__username', 'user__first_name')