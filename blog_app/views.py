from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class BlogListView(View):
    def get(self, request: HttpRequest):
        return render(request,template_name='blog_app/list_blog.html')
