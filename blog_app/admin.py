from django.db.models import Q
from django.contrib import admin
from .models import Article, ArticleTag, ArticleComment, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

    def has_add_permission(self, request):
        # فقط admin/editor اجازه افزودن دارند
        if request.user.groups.filter(name='subscriber').exists():
            return False
        return request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists()

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        return request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        return request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists()


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # همه کاربران (حتی نویسنده و viewer) همه تگ‌ها را می‌بینند
        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['subscriber', 'viewer']).exists():
            return False
        if obj is None:
            return True
        return request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        if obj is None:
            return True
        return request.user.is_superuser or request.user.groups.filter(name__in=['editor']).exists()

    def has_add_permission(self, request):
        if request.user.groups.filter(name__in=['subscriber']).exists():
            return False
        return True


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'is_active', 'create_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists():
            return qs
        if request.user.groups.filter(name='subscriber').exists():
            # Viewer فقط مقالات منتشرشده را می‌بیند
            return qs.filter(status='published')
        # نویسنده: فقط مقالات خودش و مقالات منتشرشده‌ی دیگران
        return qs.filter(Q(author=request.user) | Q(status='published'))

    def has_add_permission(self, request):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        if obj is None:
            return True
        if request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists():
            return True
        return obj.author == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        if obj is None:
            return True
        return (
            obj.author == request.user or
            request.user.is_superuser or
            request.user.groups.filter(name__in=['editor', 'admin']).exists()
        )

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'text', 'create_date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name__in=['editor', 'admin']).exists():
            return qs
        if request.user.groups.filter(name='subscriber').exists():
            return qs.filter(article__status='published')  # فقط نظرات مقالات منتشرشده
        return qs.filter(user=request.user)

    def has_add_permission(self, request):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        if obj is None:
            return True
        return (
            request.user.is_superuser or
            request.user.groups.filter(name__in=['editor', 'admin']).exists() or
            (obj.user == request.user)
        )

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='subscriber').exists():
            return False
        if obj is None:
            return True
        return (
            request.user.is_superuser or
            request.user.groups.filter(name__in=['editor', 'admin']).exists() or
            (obj.user == request.user)
        )
