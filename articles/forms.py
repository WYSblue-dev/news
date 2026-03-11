from django.forms import ModelForm
from .models import Article, Comment


class ArticleModelForm(ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "body",
        ]
        # this is new to us and important as this is what let's customize help
        # text for our forms
        help_texts = {
            "title": "Title for your article",
            "body": "Content of your article:",
        }
        labels = {
            "title": "Title Of Your Article",
            "body": "Body contents...",
        }
        # we can also add widgets here to help with styling I believe.


# this will be used for the purpose of adding a form directly to a html page for
# the logged in user to add a comment to that article. However though we need to
# add a way to be able to handle the get and post of this which we will look
# into upon adding this to the get_context_data of the detail view.
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        # note the use of this immutable tuple here in association with the form
        # seems like a really good practice and use case.
        fields = ("comment",)
        labels = {
            "comment": "New Comment",
        }
