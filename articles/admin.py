from django.contrib import admin
from .models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # quick list display in admin of fields and their values for every instance.
    list_display = [
        "title"[:50],
        "author",
        "date",
    ]
    model = Article


# there should be a default model changeform for the admin to be able to add the
# date value changing method here.

admin.site.register(Article, ArticleAdmin)
