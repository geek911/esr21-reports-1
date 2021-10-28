from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

esr21_reports = Navbar(name='esr21_reports')

no_url_namespace = True if settings.APP_NAME == 'esr21_reports' else False

esr21_reports.append_item(
    NavbarItem(name='Reports',
               label='Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_reports_home_url'))

esr21_reports.append_item(
    NavbarItem(name='Screening Reports',
               label='Screening Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_screening_reports_url'))

esr21_reports.append_item(
    NavbarItem(name='Consent Reports',
               label='Consent Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_consent_reports_url'))

esr21_reports.append_item(
    NavbarItem(name='Vaccination Reports',
               label='Vaccination Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_vaccine_reports_url'))

esr21_reports.append_item(
    NavbarItem(name='Adverse Events Reports',
               label='Adverse Events Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_ae_reports_url'))

site_navbars.register(esr21_reports)