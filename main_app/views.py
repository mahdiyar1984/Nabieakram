from django.contrib import messages
from django.db.models import QuerySet, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from blog_app.models import ArticleCategory
from main_app.forms import ContactUsModelForm
from main_app.models import SiteSetting, ContactUs, FooterLink, FooterLinkBox, Slider


def site_header_component(request):
    site_setting: SiteSetting = SiteSetting.objects.all().first()
    context = {
        'site_settings': site_setting,
    }
    return render(request, 'shared/site_header_component.html', context)
def site_footer_component(request):
    footer_link_boxes: QuerySet[FooterLinkBox] = FooterLinkBox.objects.all()
    site_setting: SiteSetting = SiteSetting.objects.all().first()
    context = {
        'footer_link_boxes': footer_link_boxes,
        'site_settings': site_setting,
    }
    return render(request, 'shared/site_footer_component.html', context)
def index(request):
    sliders: QuerySet[Slider] = Slider.objects.filter(is_active=True).order_by("order")
    site_setting: SiteSetting = SiteSetting.objects.all().first()
    article_categories = (
        ArticleCategory.objects
        .filter(parent__isnull=True)
        .annotate(article_count=Count("article"))
        .order_by("-article_count")[:6]
    )
    context = {
        'sliders': sliders,
        'site_settings': site_setting,
        'article_categories': article_categories
    }
    return render(request, "main_app/index.html", context)
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
        context['site_settings'] = setting
        return context
class TimeTableView(TemplateView):
    template_name = 'main_app/time_table_heiat.html'