from django.db import models
from django.urls import reverse

# there are a couple main reasons we use the import from our django settings(conf)
# 1. if we were to do something like accounts.User it would be pointing at the
# wrong model.(That would be the default django model).
# 2. importing lets us use the proper model, even in the case of if the model
# changes later... since we're pointing at the setting constant this will be
# more flexible in that sense now.
# 3. if we were to use the get_user_model that can run into circular import
# issues which we don't ever want obviously.(middle of loading apps and models
# so trying to call a model on this apps import initilization isn't wise!!!)
# (it should be noted that what is really being passed in the accounts.CustomUser)
# str from the settings but this convention is more robust because as stated if
# the accounts model were to ever to be changed it would auto update here.
from django.conf import settings


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        # note that we use the real import to be able to use this model.
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # this dunder str method is great because it lets us see the obj by its
    # its title field value not the obj representation in memory.
    def __str__(self):
        # should only take us to the 50th character and then adds a elllipise
        if len(self.title) > 50:
            return f"{self.title[:50]}..."
        else:
            return self.title

    # get ab url is great because it lets us avoid hard coding urls in html page
    # since in a for loop more than likly the user will be working with this obj
    # instance directly we can just method call this which uses the name lookup
    # of the urls file. There is going to be an id associated with the kwargs
    # returned and that is what we will need to pass to the urls slug/convertor
    # to correctly render the new page.
    def get_absolute_url(self):
        # pk means primary key also known as an id. This instance connection
        # lets us then pass in the value the url convertor needs.
        return reverse("article_detail", kwargs={"pk": self.pk})


# it should be retouched on that there are three types of foreignkey relations
# one to one one to many and many to one.
class Comment(models.Model):
    # This is going to be the class that ties to the model comments to the
    # Article model which let's the user then add comments to posted articles.
    # We will also want to be able to let the user who creates the comment to
    # be able to edit it. Maybe not delete it however.
    # The viewing functionality can be done throough security as well as the
    # htmltemplate itself
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    # using the character field here is nice because it limits the amount of
    # text the user cant enter. This means maybe we can display this?
    comment = models.CharField(max_length=140)
    date_added = models.DateTimeField(auto_now_add=True)
    # this gives us the corerct spelling to be displayed in the admin interface
    VERBOSE_NAME_PLURAL = "comments"

    def __str__(self):
        return f"{self.comment[:15]}..."

    def get_absolute_url(self):
        # pointing to article_list makes sense because that is where the
        # comments will reside. The won't have their own page. Only a form page
        return reverse("article_list")
