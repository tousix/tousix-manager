# -*- coding: utf8 -*-
__author__ = 'remy'

import json
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from database.models import Regles, Switch
from Deployment.forms import ConfirmForm
from Deployment.rules import RulesDeployment
from django.shortcuts import render, Http404
from Authentication.AdminMixin import AdminVerificationMixin
from Authentication.AddressMixin import AddressLimitationMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Deployment.JSONResponseMixin import JSONResponseMixin


class RulesDeploymentConfirmView(AdminVerificationMixin, FormView):

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
