from django import forms
from main_app.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'subject', 'message']
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

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if len(full_name) < 3:
            raise forms.ValidationError("اسم باید حداقل ۳ کاراکتر باشد.")
        return full_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith(".com"):
            raise forms.ValidationError("ایمیل باید با .com تمام شود.")
        return email

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")
        banned_words = ["spam", "test"]
        if any(word in subject.lower() for word in banned_words):
            raise forms.ValidationError("موضوع شامل کلمات غیرمجاز است.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message.split()) < 5:
            raise forms.ValidationError("پیام باید حداقل ۵ کلمه داشته باشد.")
        return message
