# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import FormView
from database.models import Regles, Switch
from Deployment.forms import ConfirmForm
from Deployment.rules import RulesDeployment
from django.shortcuts import render

class RulesDeploymentConfirmView(FormView):

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
