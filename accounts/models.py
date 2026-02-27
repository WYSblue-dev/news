from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    # remember that we set the db to equate a empty integer value as null
    age = models.PositiveIntegerField(null=True, blank=True)
