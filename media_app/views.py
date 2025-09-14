from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class GalleryView(View):
    def get(self, request):
        return render(request, 'media_app/gallery.html')


class LectureListView(View):
    def get(self, request):
        return render(request, 'media_app/lecture_List_page.html')


class LectureDetailView(View):
    def get(self, request, pk):
        return render(request, 'media_app/lecture_Detail_page.html')
