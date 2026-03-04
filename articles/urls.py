from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("<int:pk>/detail/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
]
