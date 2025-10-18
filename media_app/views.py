from django.contrib import messages
from django.db.models import QuerySet, Q
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from media_app.models import GalleryImage, GalleryCategory, Lecture, LectureClip, LectureCategory, LectureComment


class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'media_app/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True, is_delete=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = GalleryCategory.objects.filter(is_active=True, is_delete=False)
        return context


class LectureListView(ListView):
    model = Lecture
    template_name = 'media_app/lecture_List_page.html'
    context_object_name = 'lectures'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category_id = self.request.GET.get('category')
        tag_id = self.request.GET.get('tag')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )
        if category_id:
            queryset = queryset.filter(selected_categories__id=category_id)

        if tag_id:
            queryset = queryset.filter(selected_tags=tag_id)

        return queryset


class SearchLectureView(View):
    def get(self, request: HttpRequest):
        return render(request, template_name='media_app/components/search.html')


class CategoryLecturesView(View):
    def get(self, request: HttpRequest):
        categories: QuerySet[LectureCategory] = LectureCategory.objects.filter(parent__isnull=True).prefetch_related(
            "lecturecategory_set")
        context = {
            'categories': categories,
        }
        return render(request, template_name='media_app/components/category.html', context=context)


class ArchiveLecturesView(View):
    def get(self, request: HttpRequest):
        lectures: QuerySet[Lecture] = Lecture.objects.filter(is_active=True)
        context = {
            'lectures': lectures,
        }
        return render(request, template_name='media_app/components/archive.html', context=context)


class RecentLecturesView(View):
    def get(self, request: HttpRequest):
        lectures: QuerySet[Lecture] = Lecture.objects.filter(is_active=True).order_by('-created_date')[:3]
        context = {
            'lectures': lectures,
        }
        return render(request, template_name='media_app/components/recent_lectures.html', context=context)


class LectureDetailView(View):
    def get(self, request: HttpRequest, pk):
        lecture: Lecture = Lecture.objects.get(pk=pk, is_active=True)

        comments = LectureComment.objects.filter(
            lecture=lecture,
            parent=None
        ).filter(Q(is_active=True) | Q(user=request.user))

        temp_comment_ids = request.session.get('temp_comments', [])
        if temp_comment_ids:
            comments = comments | LectureComment.objects.filter(id__in=temp_comment_ids)

        comments = comments.distinct().order_by('-created_date')

        for comment in comments:
            replies = (comment.lecturecomment_set
                       .filter(Q(is_active=True) | Q(user=request.user))
                       .order_by('created_date'))
            comment.replies = replies

        context = {
            'lecture': lecture,
            'comments': comments,
        }
        return render(request, 'media_app/lecture_detail_page.html', context)

    def post(self, request: HttpRequest, pk):
        lecture = get_object_or_404(Lecture, pk=pk)

        if request.user.is_authenticated:
            name = lecture.author.first_name
            email = lecture.author.email
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')

        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')

        comment = LectureComment.objects.create(
            lecture=lecture,
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

        return redirect("media_app:lecture_detail_page", pk=lecture.pk)
