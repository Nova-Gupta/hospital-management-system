from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth
    path('api/auth/register/', include('hospital.apps.accounts.urls')),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Apps
    path('api/doctors/', include('hospital.apps.doctors.urls')),
    path('api/patients/', include('hospital.apps.patients.urls')),
    path('api/appointments/', include('hospital.apps.appointments.urls')),
    path('api/prescriptions/', include('hospital.apps.prescriptions.urls')),
    path('api/billing/', include('hospital.apps.billing.urls')),
    path('api/dashboard/', include('hospital.apps.dashboard.urls')),
]