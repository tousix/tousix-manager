# -*- coding: utf8 -*-
__author__ = 'remy'

from django.http import Http404
from django.conf import settings


class AddressLimitationMixin(object):
    """
    Class used for verifying if the emitter of the request is in the IP address whitelist.

    It is only suitable for private addresses and/or LAN addresses (proxies can bypass that security
    if an public IP address is defined in the whitelist).

    You need to add a ADDRESS_WHITELIST list variable with string addresses in your django settings file.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.META["HTTP_REMOTE_ADDR"] in settings.ADDRESS_WHITELIST:
            return super(AddressLimitationMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404()
