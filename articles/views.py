from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from .models import Article
from .forms import ArticleModelForm, CommentForm

# the purpose of userpassestestmixin is to denie the wrong user from trying to
# edit a article that isn't theirs returning an http403 forbidden.
# in addition to this check and forbadding the wrong user access we can also
# simply check if the user is the auther with template if tags. Only displaying
# the edit and delete anchors if they are the author.  VERY CLEVER!!!!
from django.contrib.auth.mixins import UserPassesTestMixin

# we could have done a filter for the purpose of only displaying the users arts
# but that hinders the function of the site. That would be done with get_queryset

# if request.user != article.user raise Http404 this is an extra security step
# for when we want to check if the person accessing the edit or delete page is
# who they should be by checking the get_object. Take note this will only be
# used on particular views just like the userpasssestestmixin
from django.http import Http404


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    # keep in mind in this form is where we can edit the help text and style
    # the page better.
    form_class = ArticleModelForm
    # fields = [
    #     "title",
    #     "body",
    # ]
    template_name = "article_edit.html"

    # calls first checks filters to only user objects from db
    # 404 if mailicious
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    # 2nd in django operating order. Validates author is accessing their obj
    # raises 404 if not.
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404
        else:
            return obj

    # 3rd in the call lineup. Says this object exist but you're not allowed.
    # raises 403 forbidden
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    # calls first checks filters to only user objects from db
    # 404 if mailicious
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    # 2nd in django operating order. Validates author is accessing their obj
    # raises 404 if not.
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404
        else:
            return obj

    # 3rd in the call lineup. Says this object exist but you're not allowed.
    # raises 403 forbidden
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    # this could be a tuple
    fields = [
        "title",
        "body",
    ]
    template_name = "article_create.html"
    # we could have left this blank to be able to accomadate the get_absolute_url
    # if we didn't have the get abs we shall specify this accordingly.
    success_url = reverse_lazy("article_list")

    # form is the form that has the submitted info.
    def form_valid(self, form):
        # with the form instance we add the author to be equal to the request.user
        form.instance.author = self.request.user
        # we them make a call to the super to perform the save with the new info
        return super().form_valid(form)


# get_object by default calls with queryset=None. We setup the same on our
# override. However we repass that parameter 'queryset' that equals None to it's
# required parameter queryset. But in the parent call it realizes that the value
# is None so it calls self.get_queryset which makes the call to our override of
# get_queryset. That call returns a filtered obj based on the request.user. It
# also knows exactly what pk/obj instance it wants because of the url convertor.
# so the queryset knows what object it wants from the request. SO DOES GET_OBJ
# THIS IS DUE TO THE KWARGS THAT DJANGO USES AND HAS AVAILABLE
# That convetor recieved its value from the user and the request working with
# that specific model instance. we then check that the object we obtained that
# is fliterd is equal to the request.user, if it isn't we raise an Http404.
# After that we then move into the use of UserPassesTestMixin which just recalls
# a redundent get_object.


# will be used for the purpose of handling the get request state for the
# parent/inherited View class.
# displays an empty form
class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    # gives us access to the empty form state.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    # will be used for the purpose of rendering and handling a post request in
    # the wrapper for a View extension/inheritence cycle.
    # process the user submitted data


# used to handle the post state of the form submition from the article_detail
# page
class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "artcle_detail.html"

    # why do we pass what we do we can infer...
    def post(self, request, *args, **kwargs):
        # use get object to assign the object/Model
        self.object = self.get_object()
        # why do we pass what we do we can infer...
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        # set the model we want to tie this comment model to.
        comment.article = self.object
        # set the author of this comment to the request user.
        comment.author = self.request.user
        # save to the db
        comment.save()
        # make a call to the super form to finish its process?
        return super().form_valid(form)

    def get_success_url(self):
        # obtain the object through the object from the posted post data
        article = self.object
        # call the url by name with the proper pk from the object
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    model = Article
    template_name = "article_detail.html"

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
