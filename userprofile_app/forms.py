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

class ArticleCategoryForm(forms.Form):
    title = forms.CharField(max_length=200,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control form--control pl-3',
                            }))
    parent = forms.ModelChoiceField(queryset=ArticleCategory.objects.all(),
                                    required=False,
                                    widget=forms.Select(attrs={
                                        'class': 'form-control form--control pl-3',
                                    }))
    url_title = forms.CharField(max_length=200,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control form--control pl-3',
                                }))
    image = forms.FileField(required=False,
                            widget=forms.ClearableFileInput(attrs={
                                'class': 'multi file-upload-input with-preview MultiFile-applied',
                                'id': 'MultiFile2',
                            }))
    is_active = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(attrs={
                                       'class': 'form-check-input',
                                       'style': 'width: 1.2em; height: 1.2em; margin-top: 6px; margin-left: 8px;'
                                   }))
    is_delete = forms.BooleanField(required=False,
                                   widget=forms.CheckboxInput(attrs={
                                       'class': 'form-check-input',
                                       'style': 'width: 1.2em; height: 1.2em; margin-top: 6px; margin-left: 8px;'
                                   }))

    def clean_url_title(self):
        url_title = self.cleaned_data.get('url_title')
        if ' ' in url_title:
            raise forms.ValidationError('عنوان url نباید شامل فاصله باشد')
        return url_title

    def clean(self):
        cleaned_data = super().clean()
        is_delete = cleaned_data.get('is_delete')
        is_active = cleaned_data.get('is_active')

        if is_delete and is_active:
            raise forms.ValidationError('یک دسته بندی نمی‌تواند همزمان فعال و حذف شده باشد')
        return cleaned_data

class ArticleTagForm(forms.ModelForm):
    pass

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
