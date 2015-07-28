# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from Authentication.forms import UserCreationForm


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/create_user.html'
