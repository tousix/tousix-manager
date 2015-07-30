# -*- coding: utf8 -*-
__author__ = 'remy'

from django.contrib.auth.decorators import user_passes_test


class AdminVerificationMixin(object):

    def admin_check(user):
        return user.is_superuser

    @user_passes_test(admin_check, login_url=None, redirect_field_name=None)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminVerificationMixin, self).dispatch(request, *args, **kwargs)