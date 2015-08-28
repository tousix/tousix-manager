# -*- coding: utf8 -*-
__author__ = 'remy'

from django.http import JsonResponse
from django.utils.timezone import datetime

class JSONResponseMixin(object):
    """
    Mixin used for render statistic data into JSON-friendly response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Overwrites default method (calls render_to_json_response)
        :param context:
        :param response_kwargs:
        :return:
        """
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Render a JSON HTTP Response
        :param context:
        :param response_kwargs:
        :return:
        """
        return JsonResponse(context, safe=False, **response_kwargs)
