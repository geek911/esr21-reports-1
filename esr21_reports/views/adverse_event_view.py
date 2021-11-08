from django.core.paginator import Paginator
from django.apps import apps as django_apps
from django.views.generic.list import ListView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from esr21_subject.models import EligibilityConfirmation



class AdverseEventView(EdcBaseViewMixin, NavbarViewMixin,ListView):
    template_name = 'safety_reports/ae_reports.html'
    navbar_name = 'esr21_reports'
    navbar_selected_item = 'Adverse Events Reports'
    model = EligibilityConfirmation

    ae_model = 'esr21_subject.adverseevent'
    sae_model = 'esr21_subject.seriousadverseevent'
    siae_model = 'esr21_subject.specialinterestadverseevent'


    @property
    def ae_cls(self):
        return django_apps.get_model(self.ae_model)
    
    @property
    def sae_cls(self):
        return django_apps.get_model(self.sae_model)

    @property
    def siae_cls(self):
        return django_apps.get_model(self.siae_model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        aes = self.ae_cls.objects.all()
        saes = self.sae_cls.objects.all()
        siaes = self.siae_cls.objects.all()


        paginator = Paginator(aes, 6)
        self.object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        gaborone_ae = aes.filter(site_id=40).count()
        maun_ae = aes.filter(site_id=41).count()
        serowe_ae = aes.filter(site_id=42).count()
        f_town_ae = aes.filter(site_id=43).count()
        phikwe_ae = aes.filter(site_id=44).count()


        gaborone_sae = saes.filter(site_id=40).count()
        maun_sae = saes.filter(site_id=41).count()
        serowe_sae = saes.filter(site_id=42).count()
        f_town_sae = saes.filter(site_id=43).count()
        phikwe_sae = saes.filter(site_id=44).count()


        gaborone_siae = siaes.filter(site_id=40).count()
        maun_siae = siaes.filter(site_id=41).count()
        serowe_siae = siaes.filter(site_id=42).count()
        f_town_siae = siaes.filter(site_id=43).count()
        phikwe_siae = siaes.filter(site_id=44).count()


        context.update(
            page_obj=page_obj,
            object_list =self.object_list,

            aes=aes,
            saes=saes,
            siaes=siaes,

            gaborone_ae=gaborone_ae,
            maun_ae=maun_ae,
            serowe_ae=serowe_ae,
            phikwe_ae=phikwe_ae,
            f_town_ae=f_town_ae,

            gaborone_sae=gaborone_sae,
            maun_sae=maun_sae,
            serowe_sae=serowe_sae,
            phikwe_sae=phikwe_sae,
            f_town_sae=f_town_sae,

            gaborone_siae=gaborone_siae,
            maun_siae=maun_siae,
            serowe_siae=serowe_siae,
            phikwe_siae=phikwe_siae,
            f_town_siae=f_town_siae,
            
        )
        return context