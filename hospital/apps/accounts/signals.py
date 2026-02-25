from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from hospital.apps.doctors.models import Doctor
from hospital.apps.patients.models import Patient

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.DOCTOR:
            Doctor.objects.create(
                user=instance,
                specialization='general',
                license_number=f'LIC-{instance.id:06d}',
            )
        elif instance.role == User.Role.PATIENT:
            Patient.objects.create(user=instance)