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
        return JsonResponse(self.refactor_json(context), safe=False, **response_kwargs)

    def refactor_json(self, context):
        """
        Adapts Python objects for JSON factoring.
        :param context:
        :return:
        """
        for data in context:
            if isinstance(data.get('time'), datetime):
                # Remove microseconds & Transforms into ISO 8601 format
                data['time'] = data['time'].replace(microsecond=0).isoformat()
        return context
