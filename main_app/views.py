from django.shortcuts import render


def index(request):
    return render(request, "main_app/index.html")


def site_header_component(request):
    return render(request, 'shared/site_header_component.html')


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html')
