# -*- coding: utf8 -*-
__author__ = 'remy'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Thanks to : http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# For clean implementation of this decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

