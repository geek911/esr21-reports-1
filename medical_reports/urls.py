from django.urls import path
from . import views


app_name = 'medical_reports'

urlpatterns = [
    path('advent/', views.adverse_event_report_page, name='advent'),
    path('vaccination/', views.vaccination_report_page, name='vaccination'),
]
