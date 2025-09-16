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

    # def get_context_data(self, **kwargs):
    #     context: dict[str, any] = super().get_context_data(**kwargs)
    #     site_setting: SiteSetting = SiteSetting.objects.filter(is_main_sitting=True).first()
    #     context['site_setting'] = site_setting
    #     return context

# class ContactUsView(CreateView):
#     model = ContactUs
#     fields = []
#     template_name = 'main_app/contact_us_page.html'
#     success_url = reverse_lazy('main_app:contact_us_page')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         setting: SiteSetting = SiteSetting.objects.all().first()
#         context['site_setting'] = setting
#         return context
#
#     def get(self, request, *arg, **kwargs):
#         self.object = None
#         return self.render_to_response(self.get_context_data())
#
#     def post(self, request, *args, **kwargs):
#         full_name = request.POST.get('full_name', '').strip()
#         subject = request.POST.get('subject', '').strip()
#         email = request.POST.get('email', '').strip()
#         message = request.POST.get('message', '').strip()
#
#         # validate form
#         errors = {}
#         if not full_name:
#             errors['full_name'] = "Full name is required."
#         if not subject:
#             errors['subject'] = "Subject is required."
#         if not email:
#             errors['email'] = "Email is required."
#         if not message:
#             errors['message'] = "Message is required."
#
#         if errors:
#             self.object = None
#             return self.render_to_response(self.get_context_data(
#                 errors=errors,
#                 full_name=full_name,
#                 subject=subject,
#                 email=email,
#                 message=message))
#
#         self.object = ContactUs.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             full_name=full_name,
#             subject=subject,
#             email=email,
#             message=message
#         )
#
#         return self.render_to_response(self.get_context_data(success=True))
class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'main_app/contact_us_page.html'
    success_url = reverse_lazy('main_app:contact_us_page')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            form.instance.full_name = self.request.user.get_full_name()
            form.instance.email = self.request.user.email

        response = super().form_valid(form)
        messages.success(self.request, "پیام شما با موفقیت ارسال شد!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً خطاهای فرم را بررسی کنید.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.all().first()
        context['site_setting'] = setting
        return context
