from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to="images/profile", null=True, blank=True, verbose_name="تصویر آواتار")
    email_activation_code = models.CharField(max_length=64, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='شماره تماس')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        return self.email