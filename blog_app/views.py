from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from blog_app.models import Article, ArticleCategory


class BlogListView(View):
    def get(self, request: HttpRequest):
        articles:QuerySet[Article] = Article.objects.filter(is_active=True)

        if request.GET.get('search'):
            articles:QuerySet[Article] = articles.filter(title__icontains=request.GET.get('search'))

        if request.GET.get('category'):
            articles:QuerySet[Article] = articles.filter(selected_categories__id=request.GET.get('category'))

        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/blog_list_page.html', context=context)

class SearchArticlesView(View):
    def get(self, request: HttpRequest):
        return render(request,template_name='blog_app/components/search.html')

class CategoryArticlesView(View):
    def get(self, request: HttpRequest):
        categories: QuerySet[ArticleCategory] =  ArticleCategory.objects.filter(parent__isnull=True).prefetch_related("articlecategory_set")
        context = {
            'categories': categories,
        }
        return render(request,template_name='blog_app/components/category.html', context=context)

class ArchiveArticlesView(View):
    def get(self, request: HttpRequest):
        return render(request,template_name='blog_app/components/archive.html')

class RecentArticlesView(View):
    def get(self, request: HttpRequest):
        return render(request,template_name='blog_app/components/recent_articles.html')

class BlogDetailView(View):
    def get(self, request: HttpRequest, pk):
        article:Article = Article.objects.get(pk=pk,is_active=True)
        context = {
            'article': article,
        }
        return render(request, template_name='blog_app/blog_detail_page.html',context=context)