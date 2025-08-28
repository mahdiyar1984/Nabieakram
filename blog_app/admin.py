from django.contrib import admin

from blog_app.models import ArticleTag, Article, ArticleCategory

admin.site.register(ArticleTag)
admin.site.register(Article)
admin.site.register(ArticleCategory)
