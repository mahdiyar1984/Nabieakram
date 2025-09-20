from django.contrib import admin
from media_app.models import GalleryCategory, GalleryImage, LectureClip, LectureCategory, Lecture, LectureTag, \
    LectureComment

admin.site.register(GalleryCategory)
admin.site.register(GalleryImage)
admin.site.register(LectureCategory)
admin.site.register(LectureTag)
admin.site.register(Lecture)
admin.site.register(LectureClip)
admin.site.register(LectureComment)
