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

from django.shortcuts import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from tousix_manager.Authentication.AddressMixin import AddressLimitationMixin
from tousix_manager.Log_Statistics.flows import FlowProcess


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
            if request.GET.__contains__("time"):
                process = FlowProcess()
                process.decode_request(data, request.GET.__getitem__("time"))
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        elif request.method == "GET":
            return HttpResponse(status=200)
