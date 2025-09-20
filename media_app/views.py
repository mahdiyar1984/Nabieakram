from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from media_app.models import GalleryImage, GalleryCategory, Lecture, LectureClip


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



class LectureDetailView(DetailView):
    model = Lecture
    template_name = 'media_app/lecture_detail_page.html'
    context_object_name = 'lecture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clips'] = LectureClip.objects.filter(lecture=self.object)
        return context
