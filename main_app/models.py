from django.db import models
from account_app.models import User
from config_app import settings


class FooterLinkBox(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    objects = models.Manager()
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی',
                                        related_name='footer_links')
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')



    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'
        ordering = ["order"]

    def __str__(self):
        return self.title


class Slider(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200, verbose_name='عنوان', null=True, blank=True)
    url = models.URLField(max_length=500, verbose_name='لینک', null=True, blank=True)
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات اسلایدر', null=True, blank=True)
    image = models.ImageField(upload_to='sliders/images', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین بروزرسانی")

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title if self.title else f"اسلاید {self.id}"


class ContactUs(models.Model):
    objects = models.Manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="contact_messages", verbose_name="کاربر")
    full_name = models.CharField(max_length=100, verbose_name="نام")
    subject = models.CharField(max_length=300, verbose_name="عنوان")
    email = models.EmailField(max_length=300, verbose_name="ایمیل")
    message = models.TextField(verbose_name="متن تماس با ما")
    created_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.TextField(verbose_name='متن پاسخ تماس با ما', null=True, blank=True)
    response_date = models.DateTimeField(null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'


class SiteSetting(models.Model):
    objects = models.Manager()

    address = models.TextField(verbose_name="آدرس")
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name="فکس")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="تلفن ثابت")
    mobile = models.CharField(max_length=20, blank=True, null=True, verbose_name="موبایل")
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="ایمیل")

    # موقعیت مکانی
    latitude = models.CharField(blank=True, null=True, verbose_name="عرض جغرافیایی")
    longitude = models.CharField(blank=True, null=True, verbose_name="طول جغرافیایی")
    map_embed = models.TextField(blank=True, null=True, verbose_name="کد نقشه (iframe)")

    # لینک‌های مسیریاب
    google_maps_link = models.URLField(blank=True, null=True, verbose_name="لینک گوگل مپ")
    balad_link = models.URLField(blank=True, null=True, verbose_name="لینک بلد")
    neshan_link = models.URLField(blank=True, null=True, verbose_name="لینک نشان")

    site_name = models.CharField(max_length=200, verbose_name="نام سایت")
    site_url = models.URLField(verbose_name="دامنه سایت")
    copy_rights = models.TextField(verbose_name="متن کپی رایت")
    about_us_text = models.TextField(verbose_name="متن درباره ما")
    site_logo = models.ImageField(upload_to="site_logo/images/", verbose_name="لوگو")
    working_hours = models.CharField(max_length=200, verbose_name="ساعات فعالیت", blank=True, null=True, )

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name
