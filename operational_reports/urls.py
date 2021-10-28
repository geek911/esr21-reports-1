

from django.urls import path
from . import views

app_name = 'operational_reports'

urlpatterns = [
    path('', views.operational_report_page, name='operational'),
]