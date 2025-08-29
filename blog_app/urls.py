from django.urls import path
from blog_app import views

app_name = "blog_app"
urlpatterns = [
    path('',views.BlogListView.as_view(),name='blog_list'),
    path('<int:pk>',views.BlogDetailView.as_view(),name='blog_detail'),
]