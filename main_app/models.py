from django.db import models


class ContactUs(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=300, verbose_name="عنوان")
    email = models.EmailField(max_length=300, verbose_name="ایمیل")
    full_name = models.CharField(max_length=300, verbose_name="نام و نام خانوادگی")
    message = models.TextField(verbose_name="متن تماس با ما")
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    response = models.TextField(verbose_name='متن پاسخ تماس با ما', null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'


class SiteSetting(models.Model):
    objects = models.Manager()
    site_name = models.CharField(max_length=200, verbose_name="نام سایت")
    site_url = models.CharField(max_length=200, verbose_name="دامنه سایت")
    address = models.CharField(max_length=200, verbose_name="آدرس")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="تلفن")
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name="فکس")
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name="ایمیل")
    copy_rights = models.TextField(verbose_name="متن کپی رایت")
    about_us_text = models.TextField(verbose_name="متن درباره ما")
    site_logo = models.ImageField(upload_to="site_logo/images/", verbose_name="لوگو")
    is_main_sitting = models.BooleanField(default=False, verbose_name="تنظیمات اصلی")

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


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
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی',
                                        related_name='footer_links')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='sliders/images', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title