from django.db import models
from hospital.apps.accounts.models import User

class Doctor(models.Model):
    class Specialization(models.TextChoices):
        GENERAL = 'general', 'General Physician'
        CARDIOLOGY = 'cardiology', 'Cardiology'
        NEUROLOGY = 'neurology', 'Neurology'
        ORTHOPEDICS = 'orthopedics', 'Orthopedics'
        PEDIATRICS = 'pediatrics', 'Pediatrics'
        DERMATOLOGY = 'dermatology', 'Dermatology'
        OTHER = 'other', 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=Specialization.choices)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"