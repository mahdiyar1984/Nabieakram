from django.forms import Textarea

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

# region Article Management
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'image', 'short_description', 'text', 'selected_categories', 'selected_tags',
                  'status', 'is_active', 'is_delete']


class ArticleReadOnlyForm(ArticleForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # غیرقابل ویرایش در سطح فرم
            field.disabled = True

            # اضافه کردن کلاس فرم (اگر خواستی)
            classes = field.widget.attrs.get('class', '')
            classes = (classes + ' form-control form--control pl-3').strip()
            field.widget.attrs['class'] = classes

            # برای textarea از readonly استفاده کن چون بعضی مرورگرها readonly بهتر عمل می‌کنه
            if isinstance(field.widget, Textarea):
                field.widget.attrs['readonly'] = 'readonly'
            else:
                # select, file input, inputهای دیگر
                field.widget.attrs['disabled'] = 'disabled'


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ['title', 'parent', 'url_title', 'image', 'is_active', 'is_delete']


class ArticleCategoryReadOnlyForm(ArticleCategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.disabled = True  # غیرقابل ویرایش

            # اضافه کردن کلاس فرم
            classes = field.widget.attrs.get('class', '')
            classes = (classes + ' form-control form--control pl-3').strip()
            field.widget.attrs['class'] = classes

            # برای textarea از readonly استفاده کن
            if isinstance(field.widget, Textarea):
                field.widget.attrs['readonly'] = 'readonly'
            else:
                # select و input های دیگر
                field.widget.attrs['disabled'] = 'disabled'


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ['title']  # فقط عنوان تگ
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form--control',
                'placeholder': 'عنوان تگ جدید را وارد کنید'
            })
        }


class ArticleCommentForm(forms.ModelForm):
    pass


# endregion

# region Lecture Management
class LectureForm(forms.ModelForm):
    pass


class LectureCategoryForm(forms.ModelForm):
    pass


class LectureTagForm(forms.ModelForm):
    pass


class LectureCommentForm(forms.ModelForm):
    pass


# endregion

# region Lecture Management
class GalleryImageForm(forms.ModelForm):
    pass


class GalleryCategoryForm(forms.ModelForm):
    pass


# endregion

# region Footer Link Management
class FooterLinkForm(forms.ModelForm):
    pass


class FooterLinkBoxForm(forms.ModelForm):
    pass


# endregion

# region Lecture Management
class ContactUsForm(forms.ModelForm):
    pass


# endregion

# region Slider Management
class SliderForm(forms.ModelForm):
    pass


# endregion

# region SiteSetting Management
class SiteSettingForm(forms.ModelForm):
    pass
# endregion
