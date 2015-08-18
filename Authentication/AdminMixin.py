# -*- coding: utf8 -*-
__author__ = 'remy'

from django.shortcuts import Http404


class AdminVerificationMixin(object):
    """
    This class is used for verifying the identity of the authenticated user.
    The main use for this class is for restrict sensible views.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(AdminVerificationMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404()
