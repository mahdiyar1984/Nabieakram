from django import forms
from blog_app.models import Article, ArticleCategory, ArticleTag


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
