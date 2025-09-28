from blog_app.models import Article, ArticleCategory, ArticleTag
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account_app.models import User
from django.contrib.auth.models import Group, Permission

# region group management

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

# endregion

# region user management
class UserCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar', 'about_user', 'address',
                  'groups', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    password = None  # پنهان کردن فیلد پسورد در فرم ویرایش
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar', 'about_user', 'address',
                  'groups']

# endregion

# region article management
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'image', 'short_description', 'text', 'selected_categories', 'selected_tags']
        widgets = {
            'selected_categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'selected_tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ['title']  # فقط عنوان تگ
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form--control',
                'placeholder': 'عنوان تگ جدید را وارد کنید'
            })
        }

# endregion


