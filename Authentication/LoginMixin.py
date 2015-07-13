# -*- coding: utf8 -*-
__author__ = 'remy'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Thanks to : http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# For clean implementation of this decorator

class LoginRequiredMixin(object):
    """
    This a Mixin  created for simplifying the code prensent in the other views.
    It only adds the decorator in the subclass.
    Warning: You need to inherit this class first among the others, otherwise it will be redefined by other views,
    thus erase the modification of the method.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

