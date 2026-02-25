from django.core.cache import cache
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from hospital.apps.accounts.permissions import IsAdmin
from hospital.apps.accounts.models import User
from hospital.apps.appointments.models import Appointment
from hospital.apps.billing.models import Invoice

DASHBOARD_CACHE_KEY = 'dashboard_stats'
CACHE_TIMEOUT = 60 * 5  # 5 minutes

class DashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        stats = cache.get(DASHBOARD_CACHE_KEY)

        if not stats:
            today = timezone.now().date()
            stats = {
                'total_doctors': User.objects.filter(role='doctor').count(),
                'total_patients': User.objects.filter(role='patient').count(),
                'total_appointments': Appointment.objects.count(),
                'pending_appointments': Appointment.objects.filter(status='pending').count(),
                'completed_appointments': Appointment.objects.filter(status='completed').count(),
                'total_revenue': Invoice.objects.filter(
                    payment_status='paid'
                ).aggregate(total=Sum('total_amount'))['total'] or 0,
                'monthly_appointments': Appointment.objects.filter(
                    appointment_date__month=today.month,
                    appointment_date__year=today.year
                ).count(),
            }
            cache.set(DASHBOARD_CACHE_KEY, stats, CACHE_TIMEOUT)

        return Response(stats)