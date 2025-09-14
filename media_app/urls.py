from django.urls import path
from media_app import views

app_name = "media_app"
urlpatterns = [
    path('gallery/',views.GalleryView.as_view(),name='gallery_page'),
    path('lecture/',views.LectureListView.as_view(),name='lecture_list_page'),
    path('lecture/<int:pk>/',views.LectureDetailView.as_view(),name='lecture_detail_page'),
]