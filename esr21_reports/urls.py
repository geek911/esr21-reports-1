
from django.contrib import admin
from django.urls import path
from .views import (HomeView, 
                    ScreeningView, 
                    ConsentView,
                    VaccinationView,
                    AdverseEventView,
                    ManagementReportsView,
                    DetailedAdverseEventView,
                    )

from .views import line_chart, line_chart_json


app_name = 'esr21_reports'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='esr21_reports_home_url',),
    path('screening_reports', ScreeningView.as_view(), name='esr21_screening_reports_url'),
    path('consent_reports', ConsentView.as_view(), name='esr21_consent_reports_url'),
    path('vaccine_reports', VaccinationView.as_view(), name='esr21_vaccine_reports_url'),
    path('ae_reports', AdverseEventView.as_view(), name='esr21_ae_reports_url'),
    path('ae_detailed_reports', DetailedAdverseEventView.as_view(), name='esr21_ae_detailed_reports_url'),
    path('sae_detailed_reports', AdverseEventView.as_view(), name='esr21_sae_detailed_reports_url'),
    path('siae_detailed_reports', AdverseEventView.as_view(), name='esr21_siae_detailed_reports_url'),
    path('ae_dm_reports', ManagementReportsView.as_view(), name='esr21_dm_reports_url'),
    path('dm_reports', ManagementReportsView.as_view(), name='esr21_dm_reports_url'),
    
    path('chart', line_chart, name='line_chart_url'),
    path('chartJSON', line_chart_json, name='line_chart_json_url'),
]


