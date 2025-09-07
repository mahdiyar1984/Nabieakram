from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account_app.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff','is_active')
    list_editable = ('is_active', 'is_staff','is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی',
         {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'avatar', 'about_user', 'address')}),
        ('مجوزها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
        ('کد فعالسازی ایمیل', {'fields': ('email_activation_code',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'phone_number', 'avatar')
        }),
    )
    # search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    ordering = ('id',)
    # list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
