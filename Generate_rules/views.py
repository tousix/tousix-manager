# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import FormView
from django.shortcuts import render
from Generate_rules.manager import Manager
from Generate_rules.forms import SwitchChoiceForm
from database.models import Regles


class SelectionSwitchView(FormView):
    """
    Testing view for Generate_rules app
    """
    form_class = SwitchChoiceForm
    template_name = "switches_list.html"

    def form_valid(self, form):
        switches = form.get_selected()
        manager = Manager()
        manager.create_rules(switches)
        rules = Regles.objects.values('regles')
        return render(self.request, "switches_list.html", context={"rules": rules})


