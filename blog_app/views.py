from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from blog_app.models import Article


class BlogListView(View):
    def get(self, request: HttpRequest):
        articles:QuerySet[Article] = Article.objects.filter(is_active=True)
        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/blog_list_page.html', context=context)

class BlogDetailView(View):
    def get(self, request: HttpRequest, pk):
        article:Article = Article.objects.get(pk=pk,is_active=True)
        context = {
            'article': article,
        }
        return render(request, template_name='blog_app/blog_detail_page.html',context=context)