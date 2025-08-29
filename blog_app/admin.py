from django.contrib import admin

from blog_app.models import ArticleTag, Article, ArticleCategory


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','is_active')
    list_editable = ('is_active',)

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title','parent', 'is_active')
    list_editable = ('parent','is_active')



admin.site.register(ArticleTag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(ArticleCategory,ArticleCategoryAdmin)
