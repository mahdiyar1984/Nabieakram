import jdatetime
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import messages
from django.db.models import QuerySet, Avg, Count
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from blog_app.models import Article, ArticleCategory, ArticleComment
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

from main_app.models import Rating


class BlogListView(View):
    def get(self, request: HttpRequest):
        articles: QuerySet[Article] = Article.objects.filter(is_active=True)

        article_ct = ContentType.objects.get_for_model(Article)

        # اضافه کردن امتیاز به هر مورد
        for obj in articles:
            ratings = Rating.objects.filter(content_type=article_ct, object_id=obj.id)
            obj.comment_count = ArticleComment.objects.filter(
                article=obj, is_active=True, is_delete=False, parent__isnull=False).count()
            obj.rating_count = ratings.count()
            obj.rating_avg = ratings.aggregate(Avg('score'))['score__avg'] or 0
            obj.full_stars = int(obj.rating_avg)
            obj.half_star = 1 if (obj.rating_avg - obj.full_stars) >= 0.5 else 0

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

        article_ct = ContentType.objects.get_for_model(Article)

        # اضافه کردن امتیاز به هر مورد
        for obj in articles:
            ratings = Rating.objects.filter(content_type=article_ct, object_id=obj.id)
            obj.comment_count = ArticleComment.objects.filter(
                article=obj, is_active=True, is_delete=False, parent__isnull=False).count()
            obj.rating_count = ratings.count()
            obj.rating_avg = ratings.aggregate(Avg('score'))['score__avg'] or 0
            obj.full_stars = int(obj.rating_avg)
            obj.half_star = 1 if (obj.rating_avg - obj.full_stars) >= 0.5 else 0

        context = {
            'articles': articles,
        }
        return render(request, template_name='blog_app/components/recent_articles.html', context=context)


class BlogDetailView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, is_active=True)

        # محاسبه امتیاز و تعداد رأی‌ها
        article_type = ContentType.objects.get_for_model(article)
        ratings = Rating.objects.filter(content_type=article_type, object_id=article.id)
        avg_rating = float(ratings.aggregate(avg=Avg('score'))['avg'] or 0)
        total_votes = ratings.aggregate(count=Count('id'))['count'] or 0

        # آماده‌سازی نمایش ستاره‌ها (full, half, empty)
        stars_display = []
        for i in range(1, 6):
            if avg_rating >= i:
                stars_display.append('full')
            elif avg_rating >= i - 0.5:
                stars_display.append('half')
            else:
                stars_display.append('empty')

        # محاسبه درصد هر ستاره
        star_counts = {i: 0 for i in range(1, 6)}
        for r in ratings:
            score = int(round(r.score))
            if 1 <= score <= 5:
                star_counts[score] += 1

        star_percentages = {}
        for i in range(5, 0, -1):
            star_percentages[i] = int(star_counts[i] / total_votes * 100) if total_votes else 0

        # لیست ستاره‌ها برای قالب
        star_list = [5, 4, 3, 2, 1]

        # 🔹 اینجا مهمه: ساخت دیکشنری از امتیاز کاربران
        user_ratings = {
            r.user_id: r.score
            for r in ratings
            if r.user_id is not None
        }

        # دریافت کامنت‌ها
        comments_qs = ArticleComment.objects.filter(article=article, parent=None)

        # اگر کاربر لاگین کرده، کامنت‌های خودش را هم اضافه کن
        if request.user.is_authenticated:
            comments_qs = comments_qs.filter(Q(is_active=True) | Q(user=request.user))
        else:
            comments_qs = comments_qs.filter(is_active=True)

        # حالا اگر کامنت موقتی در سشن داریم
        temp_comment_ids = request.session.get('temp_comments', [])
        if temp_comment_ids:
            comments_qs = comments_qs | ArticleComment.objects.filter(id__in=temp_comment_ids)

        # در نهایت distinct
        comments = comments_qs.distinct()

        article_comments_count = ArticleComment.objects.filter(article=article,parent__isnull=True).count()

        new_captcha = CaptchaStore.generate_key()  # تولید captcha_0
        captcha_url = captcha_image_url(new_captcha)  # مسیر تصویر

        context = {
            'article': article,
            'article_comments_count':article_comments_count,
            'comments': comments,
            'avg_rating': avg_rating,
            'stars_display': stars_display,
            'total_votes': total_votes,
            'star_percentages': star_percentages,
            'star_list': star_list,  # اضافه شد
            "captcha_key": new_captcha,
            "captcha_url": captcha_url,
            'user_ratings': user_ratings,  # 🔹 اضافه شد

        }

        return render(request, 'blog_app/blog_detail_page.html', context)

    def post(self, request: HttpRequest, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user.is_authenticated:
            name = article.author.first_name
            email = article.author.email
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')

        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

        comment = ArticleComment.objects.create(
            article=article,
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            text=message,
            parent_id=parent_id if parent_id else None,
            is_active=False
        )

        temp_comments = request.session.get('temp_comments', [])
        temp_comments.append(comment.id)
        request.session['temp_comments'] = temp_comments
        messages.info(request, 'نظر شما ثبت شد و پس از تایید مدیر نمایش داده خواهد شد. فعلاً فقط برای شما قابل مشاهده است.')

        return redirect("blog_app:blog_detail", pk=article.pk)
