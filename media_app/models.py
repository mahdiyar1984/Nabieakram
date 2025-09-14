from django.db import models
from account_app.models import User


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        abstract = True

class GalleryCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="بخش گالری")

    def __str__(self):
        return self.name

class GalleryImage(BaseModel):
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="بخش"
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="عنوان عکس")
    image = models.ImageField(upload_to="gallery/images/", verbose_name="تصویر")

    def __str__(self):
        return self.title if self.title else f"عکس {self.id}"

class LectureCategory(BaseModel):
    objects = models.Manager()
    parent = models.ForeignKey(to='LectureCategory',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, verbose_name='عنوان در url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی سخنرانی'
        verbose_name_plural = 'دسته بندی های سخنرانی'

class LectureTag(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان تگ")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="عنوان در URL")

    class Meta:
        verbose_name = 'تگ سخنرانی'
        verbose_name_plural = 'تگ های سخنرانی'

    def __str__(self):
        return self.title

class Lecture(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='سخنران')

    selected_categories = models.ManyToManyField(
        LectureCategory,
        related_name="lectures",
        verbose_name='دسته بندی ها')

    selected_tags = models.ManyToManyField(
        LectureTag,
        related_name="lectures",
        verbose_name='تگ ها')

    title = models.CharField(max_length=300, verbose_name='عنوان سخنرانی')
    slug = models.SlugField(max_length=400, db_index=True, unique=True, allow_unicode=True, verbose_name='عنوان در url')
    video = models.FileField(upload_to="lectures/videos/", blank=True, null=True, verbose_name="فیلم سخنرانی")
    audio = models.FileField(upload_to="lectures/audios/", blank=True, null=True, verbose_name="صوت سخنرانی")
    video_download_link = models.URLField(blank=True, null=True, verbose_name="لینک دانلود فیلم")
    audio_download_link = models.URLField(blank=True, null=True, verbose_name="لینک دانلود صوت")
    short_description = models.CharField(max_length=300, verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن سخنرانی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سخنرانی'
        verbose_name_plural = 'سخنرانی ها'

class LectureComment(models.Model):
    objects = models.Manager()
    parent = models.ForeignKey(to='LectureComment',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               verbose_name='والد')
    lecture = models.ForeignKey(Lecture,
                                on_delete=models.CASCADE,
                                related_name="comments",
                                verbose_name='سخنرانی')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='کاربر')

    text = models.TextField(verbose_name='متن نظر')

    def __str__(self):
        return f"{self.lecture.title} - {self.text[:30]}"

    class Meta:
        verbose_name = 'نظر سخنرانی'
        verbose_name_plural = 'نظرات سخنرانی'
