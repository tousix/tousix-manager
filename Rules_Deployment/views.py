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
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from Database.models import Regles, Switch
from Rules_Deployment.forms import ConfirmForm
from Rules_Deployment.rules import RulesDeployment
from django.shortcuts import render, Http404
from Authentication.AdminMixin import AdminVerificationMixin
from Authentication.AddressMixin import AddressLimitationMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Rules_Deployment.JSONResponseMixin import JSONResponseMixin


class RulesDeploymentConfirmView(AdminVerificationMixin, FormView):
    """
    Add a confirmation view for applying rules in the topology.
    This view is restricted for super users only.
    """
    form_class = ConfirmForm
    template_name = "rules_confirm.html"

    def get_context_data(self, **kwargs):

        context = super(RulesDeploymentConfirmView, self).get_context_data(**kwargs)
        context["rules"] = Regles.objects.values("regle")
        return context

    def form_valid(self, form):
        rules_deployment = RulesDeployment()
        context = rules_deployment.send_rules(Switch.objects.all())
        return render(self.request, "rules_success.html", context=context)


class RulesRestorationView(AddressLimitationMixin, JSONResponseMixin, ListView):
    """
    View used by the controller for asking up-to-date rules which need to be applied on a switch.
    This view use a Address limitation restriction, for using this view on some LAN only.
    """
    model = Regles

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if self.verify_address() is not None:
            raise Http404
        else:
            return super(RulesRestorationView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if "idswitch" in self.request.GET:
            return Regles.objects.filter(idswitch=self.request.GET["idswitch"]).values_list("regle", flat=True)
        else:
            return super(RulesRestorationView, self).get_queryset().values_list("regle", flat=True)
        
    def get_context_data(self, **kwargs):
        context = super(RulesRestorationView, self).get_context_data()
        liste = []
        for rule in context["object_list"]:
            liste.append(json.loads(rule))
        return liste
