

from django.urls import path
from . import views


urlpatterns = [
    path('', views.operational_report_page, name='operational'),
]