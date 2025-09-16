# from django import forms
# from main_app.models import ContactUs


# class ContactUsModelForm(forms.ModelForm):
#     class Meta:
#         model = ContactUs
#         fields = ['full_name','email', 'subject', 'message']
#         widgets = {
#             'full_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#             }),
#             'subject': forms.TextInput(attrs={
#                 'class': 'form-control',
#             }),
#             'message': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': '5',
#                 'id': 'message',
#             })
#         }
#         error_messages = {
#             'full_name': {
#                 'required': 'نام و نام خانوادگی اجباری می باشد. لطفا وارد کنید'
#             }
#         }