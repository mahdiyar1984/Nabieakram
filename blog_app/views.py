from django.db.models import QuerySet
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from blog_app.models import Article, ArticleCategory
from django.core.paginator import Paginator


class BlogListView(View):
    def get(self, request: HttpRequest):
        articles: QuerySet[Article] = Article.objects.filter(is_active=True)

        if request.GET.get('search'):
            articles: QuerySet[Article] = articles.filter(
                Q(title__contains=request.GET.get('search')) | Q(text__contains=request.GET.get('search')))

        if request.GET.get('category'):
            articles: QuerySet[Article] = articles.filter(selected_categories__id=request.GET.get('category'))

        if request.GET.get('archive'):
            articles: QuerySet[Article] = articles.filter(create_date__month=request.GET.get('archive'))

        paginator = Paginator(articles, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        show_pagination = page_obj.paginator.num_pages > 1

        context = {
            'page_obj': page_obj,
            'show_pagination': show_pagination,
        }
        return render(request, template_name='blog_app/blog_list_page.html', context=context)


class SearchArticlesView(View):
    def get(self, request: HttpRequest):
        return render(request, template_name='blog_app/components/search.html')


class CategoryArticlesView(View):
    def get(self, request: HttpRequest):
        categories: QuerySet[ArticleCategory] = ArticleCategory.objects.filter(parent__isnull=True).prefetch_related(
            "articlecategory_set")
        context = {
            'categories': categories,
        }
        return render(request, template_name='blog_app/components/category.html', context=context)


class ArchiveArticlesView(View):
    def get(self, request: HttpRequest):
        articles: QuerySet[Article] = Article.objects.filter(is_active=True)
        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/components/archive.html', context=context)


class RecentArticlesView(View):
    def get(self, request: HttpRequest):
        articles: QuerySet[Article] = Article.objects.filter(is_active=True).order_by('-create_date')[:2]
        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/components/recent_articles.html', context=context)


class BlogDetailView(View):
    def get(self, request: HttpRequest, pk):
        article: Article = Article.objects.get(pk=pk, is_active=True)
        context = {
            'article': article,
        }
        return render(request, template_name='blog_app/blog_detail_page.html', context=context)
