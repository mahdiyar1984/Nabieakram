from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import QuerySet, Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from blog_app.models import ArticleCategory
from main_app.forms import ContactUsModelForm
from main_app.models import SiteSetting, FooterLinkBox, Slider
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from media_app.models import Lecture
from .models import Rating
from blog_app.models import Article
from django.db.models import Avg



def site_header_component(request):
    site_setting: SiteSetting = SiteSetting.objects.all().first()
    context = {
        'site_settings': site_setting,
    }
    return render(request, 'shared/site_header_component.html', context)

def site_footer_component(request):
    footer_link_boxes: QuerySet[FooterLinkBox] = FooterLinkBox.objects.all()
    context = {
        'footer_link_boxes': footer_link_boxes,
    }
    return render(request, 'shared/site_footer_component.html', context)

def index(request):
    sliders: QuerySet[Slider] = Slider.objects.filter(is_active=True).order_by("order")
    site_setting: SiteSetting = SiteSetting.objects.all().first()
    article_categories = (
        ArticleCategory.objects
        .filter(parent__isnull=True)
        .annotate(article_count=Count("article"))
        .order_by("-article_count")[:6]
    )
    context = {
        'sliders': sliders,
        'site_settings': site_setting,
        'article_categories': article_categories
    }
    return render(request, "main_app/index.html", context)
class AboutView(TemplateView):
    template_name = 'main_app/about_page.html'

    def get_context_data(self, **kwargs):
        pass

class ContactUsPageView(FormView):
    template_name = 'main_app/contact_us_page.html'  # مسیر قالب شما
    form_class = ContactUsModelForm
    success_url = reverse_lazy('main_app:contact_us_page')

    def form_valid(self, form):
        # ذخیره فرم در مدل
        form.save()
        messages.success(self.request, "پیام شما با موفقیت ارسال شد.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً فرم را به درستی پر کنید.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.all().first()
        context['site_setting'] = site_setting
        return context

class TimeTableView(TemplateView):
    template_name = 'main_app/time_table_heiat.html'

class RateArticleView(View):
    def post(self,request):
        score = int(request.POST.get('score', 0))
        article_id = int(request.POST.get('article_id'))
        article = Article.objects.get(id=article_id)

        content_type = ContentType.objects.get_for_model(article)
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            content_type=content_type,
            object_id=article.id,
            defaults={'score': score}
        )

        average = Rating.objects.filter(content_type=content_type, object_id=article.id).aggregate(avg_score=Avg('score'))['avg_score']
        return JsonResponse({'average': average, 'score': score})
class RateLectureView(View):
    def post(self,request):
        score = int(request.POST.get('score', 0))
        lecture_id = int(request.POST.get('lecture_id'))
        lecture = Lecture.objects.get(id=lecture_id)

        content_type = ContentType.objects.get_for_model(lecture)
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            content_type=content_type,
            object_id=lecture.id,
            defaults={'score': score}
        )

        average = Rating.objects.filter(content_type=content_type, object_id=lecture.id).aggregate(avg_score=Avg('score'))['avg_score']
        return JsonResponse({'average': average, 'score': score})

class SearchView(View):
    def get(self, request):
        query = request.GET.get('search', '').strip()

        articles = []
        lectures = []

        if query:
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            )
            lectures = Lecture.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            )

            for a in articles:
                a.type = 'article'
            for l in lectures:
                l.type = 'lecture'

        # ترکیب نتایج
        results = sorted(
            list(articles) + list(lectures),
            key=lambda x: getattr(x, 'create_date', getattr(x, 'created_date', None)),
            reverse=True
        )

        # کش کردن contenttypes برای سرعت و دقت
        article_ct = ContentType.objects.get_for_model(Article)
        lecture_ct = ContentType.objects.get_for_model(Lecture)

        # اضافه کردن امتیاز به هر مورد
        for obj in results:
            if isinstance(obj, Article):
                ct = article_ct
            else:
                ct = lecture_ct

            ratings = Rating.objects.filter(content_type=ct, object_id=obj.id)
            obj.rating_count = ratings.count()
            obj.rating_avg = ratings.aggregate(Avg('score'))['score__avg'] or 0
            obj.full_stars = int(obj.rating_avg)
            obj.half_star = 1 if (obj.rating_avg - obj.full_stars) >= 0.5 else 0

        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'query': query,
            'page_obj': page_obj,
        }
        return render(request, 'main_app/search_page.html', context)

