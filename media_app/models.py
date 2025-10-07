from django.db import models
from account_app.models import User


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        abstract = True


class GalleryCategory(BaseModel):
    objects = models.Manager()
    name = models.CharField(max_length=100, unique=True, verbose_name="دسته بندی")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="اسلاگ", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی تصاویر'
        verbose_name_plural = 'دسته بندهای تصاویر'
class GalleryImage(BaseModel):
    objects = models.Manager()
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

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


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
class LectureTag(BaseModel):
    objects = models.Manager()
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان تگ")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="عنوان در URL")

    class Meta:
        verbose_name = 'تگ سخنرانی'
        verbose_name_plural = 'تگ های سخنرانی'

    def __str__(self):
        return self.title
class Lecture(BaseModel):
    objects = models.Manager()

    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('pending', 'در انتظار تأیید'),
        ('published', 'منتشر شده'),
        ('rejected', 'رد شده'),
    ]
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
    image = models.ImageField(upload_to="lectures/images/", verbose_name="تصویر")
    video = models.FileField(upload_to="lectures/videos/", blank=True, null=True, verbose_name="فیلم سخنرانی")
    audio = models.FileField(upload_to="lectures/audios/", blank=True, null=True, verbose_name="صوت سخنرانی")
    video_url = models.URLField(blank=True, null=True, verbose_name="لینک ویدیو خارجی")
    audio_url = models.URLField(blank=True, null=True, verbose_name="لینک صوت خارجی")
    short_description = models.CharField(max_length=300, null=True, blank=True, verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن سخنرانی')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='وضعیت انتشار')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'سخنرانی'
        verbose_name_plural = 'سخنرانی ها'
        permissions = [
            ("can_publish_article", "Can publish article"),
            ("can_reject_article", "Can reject article"),
        ]

class LectureClip(BaseModel):
    objects = models.Manager()
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="clips",
        verbose_name="سخنرانی اصلی"
    )
    title = models.CharField(max_length=300, verbose_name='عنوان کلیپ')
    slug = models.SlugField(max_length=400, db_index=True, unique=True, allow_unicode=True, verbose_name='عنوان در url')
    video = models.FileField(upload_to="lectures/videos/", blank=True, null=True, verbose_name="فیلم کلیپ")
    video_url = models.URLField(blank=True, null=True, verbose_name="لینک ویدیو خارجی")
    short_description = models.CharField(max_length=300, verbose_name='توضیحات کوتاه')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'کلیپ'
        verbose_name_plural = 'کلیپ ها'
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
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f"{self.lecture.title} - {self.text[:30]}"

    class Meta:
        verbose_name = 'نظر سخنرانی'
        verbose_name_plural = 'نظرات سخنرانی'
