from django.forms import Textarea
from blog_app.models import Article, ArticleCategory, ArticleTag
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account_app.models import User
from django.contrib.auth.models import Group, Permission

from main_app.models import FooterLinkBox, FooterLink, Slider, ContactUs
from media_app.models import Lecture, LectureTag, LectureCategory, LectureClip, GalleryCategory, GalleryImage


# region Article Management
class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    selected_tags = forms.ModelMultipleChoiceField(
        queryset=ArticleTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    selected_categories = forms.ModelMultipleChoiceField(
        queryset=ArticleCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Article
        fields = ['title', 'slug', 'image', 'short_description', 'text', 'selected_categories', 'selected_tags',
                  'status', 'is_active', 'is_delete']
        widgets = {
            # text input ها
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),

            # textarea ها
            'short_description': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3',
                'rows': 4
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3',
                'rows': 15
            }),

            # status با select مثل template
            'status': forms.Select(choices=[('draft', 'پیش‌نویس'), ('published', 'منتشر شده')],
                                   attrs={'class': 'form-control form--control pl-3'}),

            # boolean ها با checkbox (اگر لازم شد می‌تونید widget = CheckboxInput)
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'file-upload-input',
                'id': 'customFileInput'
            }),

        }


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


class ArticleTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = ArticleTag
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# endregion

# region Lecture Management
class LectureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    selected_tags = forms.ModelMultipleChoiceField(
        queryset=LectureTag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    selected_categories = forms.ModelMultipleChoiceField(
        queryset=LectureCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Lecture
        fields = [
            'title', 'slug', 'short_description', 'text', 'status',
            'image', 'video', 'audio', 'video_url', 'audio_url',
            'selected_categories', 'selected_tags', 'is_active', 'is_delete'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3', 'rows': 4}),
            'text': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3', 'rows': 15}),
            'status': forms.Select(choices=[
                ('draft', 'پیش‌نویس'),
                ('pending', 'در انتظار تأیید'),
                ('published', 'منتشر شده'),
                ('rejected', 'رد شده'),
            ], attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'file-upload-input',
                'id': 'customFileInput'
            }),

            'video': forms.ClearableFileInput(attrs={
                'class': 'file-upload-input',
                'id': 'customFileInput'
            }),
            'audio': forms.ClearableFileInput(attrs={
                'class': 'file-upload-input',
                'id': 'customFileInput'
            }),
            'video_url': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'audio_url': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
        }


class LectureCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = LectureCategory
        fields = ['title', 'slug', 'parent', 'is_active', 'is_delete']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'parent':forms.Select(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LectureTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = LectureTag
        fields = ['title', 'slug', 'is_active', 'is_delete']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LectureClipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = LectureClip
        fields = [
            'title','lecture', 'slug', 'short_description', 'video', 'video_url', 'is_active', 'is_delete']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'lecture': forms.Select(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'video': forms.ClearableFileInput(attrs={
                'class': 'file-upload-input',
                'id': 'customFileInput'
            }),
            'video_url': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
        }

# endregion

# region Gallery Management
class GalleryImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = GalleryImage
        fields = ['title', 'category', 'is_active', 'is_delete','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'category': forms.Select(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id': 'customFileInput'}),
        }


class GalleryCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = GalleryCategory
        fields = ['name', 'slug', 'is_active', 'is_delete']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_delete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# endregion

# region Footer Link Management
class FooterLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = FooterLink
        fields = ['title', 'footer_link_box', 'order', 'url', 'is_active']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'footer_link_box': forms.Select(attrs={'class': 'form-control form--control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control form--control pl-3'}),
            'url': forms.URLInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FooterLinkBoxForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = FooterLinkBox
        fields = ['title','is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# endregion

# region Contact Us Management
class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = ContactUs
        fields = ['full_name', 'user', 'subject', 'email', 'message',
                  'response', 'response_date', 'is_read_by_admin','is_replied']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'user': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'subject': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'email': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3',
                'rows': 5
            }),
            'response': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3',
                'rows': 5
            }),
            'response_date': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),

            'is_read_by_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_replied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }


# endregion

# region Slider Management
class SliderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        read_only = kwargs.pop('read_only', False)
        super().__init__(*args, **kwargs)

        if read_only:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = Slider
        fields = ['title','url_title','url','description','image','order','is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form--control pl-3'}),
            'url_title': forms.URLInput(attrs={'class': 'form-control form--control pl-3'}),
            'url': forms.URLInput(attrs={'class': 'form-control form--control pl-3'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control form--control user-text-editor pl-3',
                'rows': 4
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control form--control pl-3'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'file-upload-input', 'id': 'customFileInput'}),
        }


# endregion

# region SiteSetting Management
class SiteSettingForm(forms.ModelForm):
    pass
# endregion

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
