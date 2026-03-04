from django.forms import ModelForm
from .models import Article


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
