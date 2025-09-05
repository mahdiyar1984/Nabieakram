from django import forms

class ArticleCommentForm(forms.Form):
    message = forms.CharField(label="پیام", widget=forms.Textarea)