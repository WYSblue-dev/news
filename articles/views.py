from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from .models import Article
from .forms import ArticleModelForm


# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleModelForm
    # fields = [
    #     "title",
    #     "body",
    # ]
    template_name = "article_edit.html"


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")


class ArticleCreateView(CreateView):
    model = Article
    fields = [
        "title",
        "body",
        "author",
    ]
    template_name = "article_create.html"
    # we could have left this blank to be able to accomadate the get_absolute_url
    # if we didn't have the get abs we shall specify this accordingly.
    success_url = reverse_lazy("article_list")
