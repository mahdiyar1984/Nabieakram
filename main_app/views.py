from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from main_app.forms import ContactUsModelForm
from main_app.models import SiteSetting, ContactUs


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')


def index(request):
    return render(request, "main_app/index.html")


class AboutView(TemplateView):
    template_name = 'main_app/about_page.html'

    def get_context_data(self, **kwargs):
        pass


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'main_app/contact_us_page.html'
    success_url = reverse_lazy('main_app:contact_us_page')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.full_name = self.request.user.get_full_name()
            form.instance.email = self.request.user.email

        messages.success(self.request, "پیام شما با موفقیت ارسال شد!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً خطاهای فرم را بررسی کنید.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.all().first()
        context['site_setting'] = setting
        return context
