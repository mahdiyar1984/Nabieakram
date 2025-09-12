from django.urls import path
from main_app import views

app_name = "main_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('contact-us', views.ContactUsView.as_view(), name='contact_us_page'),
    path('about-us', views.AboutView.as_view(), name='about_us_page'),
]
