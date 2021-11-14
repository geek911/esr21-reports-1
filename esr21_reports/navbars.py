from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

from .navbar_dropdown_item import NavBarDropdownItem

esr21_reports = Navbar(name='esr21_reports')

no_url_namespace = True if settings.APP_NAME == 'esr21_reports' else False

esr21_reports.append_item(
    NavbarItem(name='Reports',
               label='Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_reports_home_url'))

operational_reports = NavBarDropdownItem(
    name='operational_reports',
    label='Operational Reports',
    fa_icon='fa-cogs',
    url_name='#',
    dropdown_items={'Screening Reports': 'esr21_reports:esr21_screening_reports_url',
                    'Consent Reports': 'esr21_reports:esr21_consent_reports_url',
                    'Vaccination Reports': 'esr21_reports:esr21_vaccine_reports_url'})

esr21_reports.append_item(operational_reports)

esr21_reports.append_item(
    NavbarItem(name='Adverse Events Reports',
               label='Adverse Events Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_ae_reports_url'))

esr21_reports.append_item(
    NavbarItem(name='dm_reports',
               label='Data Management Reports',
               fa_icon='fa-cogs',
               url_name='esr21_reports:esr21_dm_reports_url'))

site_navbars.register(esr21_reports)
