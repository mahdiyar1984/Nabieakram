from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group

# فرم ایجاد کاربر
class UserCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar', 'about_user', 'address', 'groups', 'password1', 'password2']

# فرم ویرایش کاربر
class UserUpdateForm(UserChangeForm):
    password = None  # پنهان کردن فیلد پسورد در فرم ویرایش
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar', 'about_user', 'address', 'groups']
