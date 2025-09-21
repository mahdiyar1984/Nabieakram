import jdatetime
from django.db.models import QuerySet
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from blog_app.models import Article, ArticleCategory, ArticleComment
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

        if request.GET.get('tag'):
            articles: QuerySet[Article] = articles.filter(selected_tags__title=request.GET.get('tag'))



        paginator = Paginator(articles, 6)
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
        articles: QuerySet[Article] = Article.objects.filter(is_active=True).order_by('-create_date')[:3]
        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/components/recent_articles.html', context=context)

class BlogDetailView(View):
    def get(self, request: HttpRequest, pk):
        article: Article = Article.objects.get(pk=pk, is_active=True)

        comments = ArticleComment.objects.filter(article=article, parent=None, is_active=True)
        context = {
            'article': article,
            'comments': comments
        }

        return render(request, template_name='blog_app/blog_detail_page.html', context=context)

    def post(self, request:HttpRequest, pk):
        article = get_object_or_404(Article, pk=pk)
        if not request.user.is_authenticated:
            return redirect('account_app:login_page')

        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

        comment = ArticleComment.objects.create(
            article=article,
            user=request.user,
            text=message,
            parent_id=parent_id if parent_id else None
        )
        return redirect("blog_app:blog_detail", pk=article.pk)



