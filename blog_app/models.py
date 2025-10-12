from django.db import models
from account_app.models import User


class ArticleCategory(models.Model):
    objects = models.Manager()
    parent = models.ForeignKey(to='ArticleCategory',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='blog_app/article_category/images', null=True, blank=True, verbose_name='تصویر دسته بندی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class ArticleTag(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان تگ")
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')


    class Meta:
        verbose_name = 'تگ مقاله'
        verbose_name_plural = 'تگ های مقاله'

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('pending', 'در انتظار تأیید'),
        ('published', 'منتشر شده'),
        ('rejected', 'رد شده'),
    ]

    objects = models.Manager()
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    selected_tags = models.ManyToManyField(ArticleTag, verbose_name='تگ ها')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=True, verbose_name='نویسنده')
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='blog_app/images', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='وضعیت انتشار')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        permissions = [
            ("can_publish_article", "Can publish article"),
            ("can_reject_article", "Can reject article"),
        ]


class ArticleComment(models.Model):
    objects = models.Manager()
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                verbose_name='مقاله')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='کاربر')

    parent = models.ForeignKey(to='ArticleComment',
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE,
                               verbose_name='والد')

    text = models.TextField(verbose_name='متن نظر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')

    def __str__(self):
        return f"{self.article.title}"

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'
