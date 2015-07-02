# -*- coding: utf8 -*-
__author__ = 'remy'

from django.http import JsonResponse
from django.utils.timezone import datetime

class JSONResponseMixin(object):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.refactor_json(context), safe=False, **response_kwargs)

    def refactor_json(self, context):
        for data in context:
            if isinstance(data.get('time'), datetime):
                data['time'] = data.get('time').isoformat()
        return context
