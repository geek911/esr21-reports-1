from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('esr21_reports/buttons/dashboard.html')
def dashboard_button(subject_identifier):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=subject_identifier)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def odd_num(value):
    return False if (value % 2) == 0 else True


@register.filter
def map_site_id(value):
    if value == 40:
        return 'Gaborone'
    elif value == 41:
        return 'Maun'
    elif value == 42:
        return 'Serowe'
    elif value == 43:
        return 'Francistown'
    elif value == 44:
        return 'Selibe Phikwe'
    return 'No site to map'
