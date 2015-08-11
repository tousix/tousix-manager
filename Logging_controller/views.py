# -*- coding: utf8 -*-
__author__ = 'remy'

import json
import logging

from django.views.generic import View
from django.views.generic.list import ListView
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Authentication.AddressMixin import AddressLimitationMixin

from database.models import LogSwitch

LOG = logging.getLogger("Logging_controller")


class AsyncEventView(AddressLimitationMixin, View):
    """
    View for the reception of asynchronous events coming from the controller.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Direct input in the database , depending of the URL.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.verify_address() is not None:
            raise Http404
        base_path = "/event/"
        if request.method == "POST":
            path = request.path

            data = json.loads(request.body.decode(encoding='utf-8'))
            dpid = int(data.get('dpid'), 16)
            if path == base_path + "switch/enter":
                self.log_database(dpid, 'Warning', "Un switch est entré dans la topologie.", json=data)
            elif path == base_path + "switch/leave":
                self.log_database(dpid, 'Error', "Un switch est sorti de la topologie.", json=data)
            elif path == base_path + "port/modify":
                self.log_database(dpid, 'Warning', "Un port a été modifié.", json=data)
            elif path == base_path + "error":
                self.log_database(dpid, 'Error', "Une erreur a été remonté par l'agent OpenFlow.", json=data)
            elif path == base_path + "error/ryu":
                self.log_database(None, 'Error', "Erreur remonté par l'application Ryu.")
            else:
                LOG.warning("Invalid url path")
                return HttpResponse(status=404)
            return HttpResponse(status=200)

    def log_database(self, dpid, level, log, json=None):

        message = LogSwitch(idswitch_id=dpid, level=level, message=log, json=json)
        message.save()


class ShowEventView(ListView):
    """
    Testing view for log display (can be done nox in the admin panel).
    """
    model = LogSwitch
    template_name = 'log_event.html'
