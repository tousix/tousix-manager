# -*- coding: utf8 -*-
__author__ = 'remy'

from Generation.views import render_conf_members, render_conf_hosts
from django.shortcuts import render, redirect
from database.models import Hote, Membre

def generate_routeserver_conf(modeladmin, request, queryset):
    if modeladmin.model is Membre:
        data = render_conf_members(request, queryset)
        return render(request, "members_list.html", context=data)
    elif modeladmin.model is Hote:
        data = render_conf_hosts(request, queryset)
        return render(request, "members_list.html", context=data)

generate_routeserver_conf.short_description = "Générer la configuration BIRD pour la sélection"

def goto_log_switch(modeladmin, request, queryset):
    pass