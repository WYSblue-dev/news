from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    # builds the url patterns but is patient and does interfere with default
    # url patterns. This is because of how Django sets up everything
    success_url = reverse_lazy("login")
