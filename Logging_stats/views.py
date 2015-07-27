# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Logging_stats.flows import FlowProcess
from django.shortcuts import HttpResponse

import json


class RecieveStatsForm(View):
    """
    View for statistics reception, coming from the controller.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            data = json.loads(request.body.decode(encoding='utf-8'))
            process = FlowProcess()
            process.decode_request(data)
            return HttpResponse(status=200)
