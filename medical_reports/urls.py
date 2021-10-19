

from django.urls import path
from . import views


urlpatterns = [
    path('', views.adverse_event_report_page, name='medical'),
]