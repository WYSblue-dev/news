from django.contrib import admin
from .models import Article, Comment


# Register your models here.


# placement matters prior to the use of this is inlines
class CommentInline(admin.TabularInline):
    # this specifys the model we will want to display in realtion to the model
    # we have a relation to. I out case we want to stack this model comment
    # under the article admin instance in the admin interface. Hence the reason
    # we anticipate adding this to the ArticleAdmin.
    model = Comment
    # by default the amount of extra fields is by default is 3 we can change
    # this with the extra attribut.
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    # this is a new attribute that I havn't saw yet. It is probably used for the
    # purpose of how django displays the comment within the html page.
    inlines = [
        CommentInline,
    ]
    # quick list display in admin of fields and their values for every instance.
    list_display = [
        "title"[:50],
        "author",
        "date",
    ]
    # william didn't point to the model in his code but that does make the
    # most sense to me for it isn't needed but in the CustomUserAdmin he did so
    # I like this redundency and that fact that this makes the process more
    # rigid and less likely to fail.
    model = Article


# class CommentAdmin(admin.ModelAdmin):
#     list_display = [
#         "author",
#         "comment",
#         "date_added",
#     ]


# add another

# there should be a default model changeform for the admin to be able to add the
# date value changing method here.

admin.site.register(Article, ArticleAdmin)
# we could use the CommentAdmin here but I suppose that it seems not of use
# unless we can also see the article instance. Hence the reason I think that
# article inlines make sense. Good use of the finder search makes sense.
admin.site.register(Comment)


# it should be noted that there are 2 types of inlines that can be used.
# stacked and tabular. stacked gives use the rows feel whereas the tabular gives
# use the colums feel. The colums feels like it displays more information
