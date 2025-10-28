from django.urls import path
from main_app import views

app_name = "main_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.AboutView.as_view(), name='about_us_page'),
    path('contact-us/', views.ContactUsPageView.as_view(), name='contact_us_page'),
    path('time-table',views.TimeTableView.as_view(),name='table_table_page'),
    path('rate-article/', views.RateArticleView.as_view(), name='rate_article'),

]
