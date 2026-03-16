from django.db.models import Count
from django.views.generic import TemplateView

from articles.models import Article

# Create your views here.


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_articles"] = (
            Article.objects.select_related("author")
            .annotate(comment_total=Count("comment"))
            .order_by("-comment_total", "-date")[:3]
        )
        return context
