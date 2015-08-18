# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from Authentication.forms import UserCreationForm


class RegisterView(CreateView):
    """
    Simple user creation view.
    Now replaced by django-registration-redux, this view is kept for testing purposes.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'registration/create_user.html'
