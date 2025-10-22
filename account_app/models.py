from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission


class User(AbstractUser):
    avatar = models.ImageField(upload_to="images/profile", null=True, blank=True, verbose_name="تصویر آواتار")
    pending_email = models.EmailField(null=True, blank=True)
    email_activation_code = models.CharField(max_length=64, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='شماره تماس')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره شخص')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        return self.email



class DashboardPermissionView(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='dashboard_permissions')
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        verbose_name = "مجوزهای قابل نمایش در داشبورد"
        verbose_name_plural = "مجوزهای قابل نمایش در داشبوردها"

    def __str__(self):
        return f"مجوزهای داشبورد برای گروه: {self.group.name}"