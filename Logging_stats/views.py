# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Logging_stats.flows import FlowProcess
from django.shortcuts import HttpResponse, Http404
from Authentication.AddressMixin import AddressLimitationMixin
import json


class RecieveStatsForm(AddressLimitationMixin, View):
    """
    View for statistics reception, coming from the controller.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Enter in the flow process class if all the requirements are avaliable.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.verify_address() is not None:
            raise Http404
        if request.method == "POST":
            data = json.loads(request.body.decode(encoding='utf-8'))
            process = FlowProcess()
            process.decode_request(data)
            return HttpResponse(status=200)
