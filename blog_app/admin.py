from django.contrib import admin
from blog_app.models import ArticleTag, Article, ArticleCategory, ArticleComment


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'url_title', 'is_active', 'is_delete']
    list_editable = ['parent', 'url_title', 'is_active', 'is_delete']


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'is_delete']
    list_editable = ['is_active', 'is_delete']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_categories', 'get_tags', 'author', 'is_active', 'is_delete']
    list_editable = ['is_active', 'is_delete']
    filter_horizontal = ['selected_categories', 'selected_tags']  # برای انتخاب راحت دسته‌بندی و تگ‌ها

    def get_categories(self, obj):
        return ", ".join([cat.title for cat in obj.selected_categories.all()])
    get_categories.short_description = 'دسته‌بندی‌ها'
    get_categories.admin_order_field = 'selected_categories'  # اختیاری؛ برای مرتب‌سازی در admin

    def get_tags(self, obj):
        return ", ".join([tag.title for tag in obj.selected_tags.all()])
    get_tags.short_description = 'تگ‌ها'
    get_tags.admin_order_field = 'selected_tags'  # اختیاری؛ برای مرتب‌سازی در admin

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'parent', 'is_active', 'is_delete']
    list_editable = ['parent', 'is_active', 'is_delete']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)

