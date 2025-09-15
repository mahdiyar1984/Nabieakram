from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from main_app.models import SiteSetting, ContactUs
from main_app.forms import ContactUsModelForm


def index(request):
    return render(request, "main_app/index.html")


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')

class AboutView(TemplateView):
    template_name = 'main_app/about_page.html'

    # def get_context_data(self, **kwargs):
    #     context: dict[str, any] = super().get_context_data(**kwargs)
    #     site_setting: SiteSetting = SiteSetting.objects.filter(is_main_sitting=True).first()
    #     context['site_setting'] = site_setting
    #     return context

class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'main_app/contact_us_page.html'
    success_url = '/contact-us'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.all().first()
        context['site_setting'] = setting
        return context

