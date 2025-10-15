from django.urls import path
from .views import AssociazioneRegistrationView, DashboardView, ReportingView

urlpatterns = [
    path('register/', AssociazioneRegistrationView.as_view(), name='associazione_register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reporting/', ReportingView.as_view(), name='reporting'),
]