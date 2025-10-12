from django import forms
from main_app.models import ContactUs
from captcha.fields import CaptchaField

class ContactUsModelForm(forms.ModelForm):
    captcha = CaptchaField(label='عبارت امنیتی')  # اگر خواستی می‌تونی حذفش کنی

    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'subject', 'message','captcha']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form--control',
                'id': 'name',
                'type': 'text',
                'name': 'full_name',
                'placeholder': 'اسم شما',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form--control',
                'id': 'email',
                'type': 'email',
                'name': 'email',
                'placeholder': 'آدرس ایمیل',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control form--control',
                'id': 'subject',
                'type': 'text',
                'name': 'subject',
                'placeholder': 'موضوع',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form--control pl-4',
                'id': 'message',
                'name': 'message',
                'placeholder': 'پیام',
                'rows': '5',
            })
        }
