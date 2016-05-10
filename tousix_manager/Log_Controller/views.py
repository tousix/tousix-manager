#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.

import json
import logging

from django.shortcuts import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.list import ListView
from django.core.mail import mail_admins

from tousix_manager.Authentication.AddressMixin import AddressLimitationMixin
from tousix_manager.Database.models import LogSwitch

LOG = logging.getLogger("Log_Controller")


class AsyncEventView(AddressLimitationMixin, View):
    """
    View for the reception of asynchronous events coming from the controller.
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """
        Direct input in the Database , depending of the URL.
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
            #TODO simplify code
            if path == base_path + "switch/enter":
                self.log_database(dpid, 'Warning', "Un switch est entré dans la topologie.", json=data)
                self.send_admin_alert(dpid, 'Warning', "Un switch est entré dans la topologie.", data)
            elif path == base_path + "switch/leave":
                self.log_database(dpid, 'Error', "Un switch est sorti de la topologie.", json=data)
                self.send_admin_alert(dpid, 'Error', "Un switch est sorti de la topologie.", data)
            elif path == base_path + "port/modify":
                self.log_database(dpid, 'Warning', "Un port a été modifié.", json=data)
                self.send_admin_alert(dpid, 'Warning', "Un port a été modifié.", data)
            elif path == base_path + "error":
                self.log_database(dpid, 'Error', "Une erreur a été remonté par l'agent OpenFlow.", json=data)
                self.send_admin_alert(dpid, 'Error', "Une erreur a été remonté par l'agent OpenFlow.", data)
            elif path == base_path + "error/ryu":
                self.log_database(None, 'Error', "Erreur remonté par l'application Ryu.")
                self.send_admin_alert(None, 'Error', "Erreur remonté par l'application Ryu.", data)
            else:
                LOG.warning("Invalid url path")
                return HttpResponse(status=404)
            return HttpResponse(status=200)

    def log_database(self, dpid, level, log, json=None):
        """
        Stores log event in the Database.
        :param dpid: Switch datapath ID
        :param level: log level
        :param message: main message to display when retrieveing the error
        :param json: Data send by the controller, which could be used to decode the content later
        """
        message = LogSwitch(idswitch_id=dpid, level=level, message=log, json=json)
        message.save()

    def send_admin_alert(self, dpid, level, message, JSON=None):
        subject = "Evènement sur le contrôleur Ryu"
        message = "Bonjour," \
                  "\n\n Ceci est un message envoyé automatiquement par le programme TouSIX-Manager.\n" \
                  "Une alerte a été envoyé par le contrôleur Ryu. Voici les détails:\n\n" \
                  "Niveau: "+ level + "\n" \
                  "Message: " + message + "\n"

        if dpid is not None:
            message = message + "DPID du switch: " + str(dpid) + "\n"
        if JSON is not None:
            message = message + "Data JSON: \n" + json.dumps(JSON)
        mail_admins(subject, message)



class ShowEventView(ListView):
    """
    Testing view for log display (can be done nox in the admin panel).
    """
    model = LogSwitch
    template_name = 'log_event.html'
