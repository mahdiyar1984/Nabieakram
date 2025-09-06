from django import forms
from .models import ArticleComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "نظر خود را بنویسید..."}),
        }