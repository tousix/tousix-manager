# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import FormView
from django.shortcuts import render
from Rules_Generation.manager import Manager
from Rules_Generation.forms import SwitchChoiceForm
from Database.models import Regles


class SelectionSwitchView(FormView):
    """
    Testing view for Rules_Generation app
    """
    form_class = SwitchChoiceForm
    template_name = "switches_list.html"

    def form_valid(self, form):
        switches = form.get_selected()
        manager = Manager()
        manager.create_rules(switches)
        rules = Regles.objects.values('regles')
        return render(self.request, "switches_list.html", context={"rules": rules})


