# -*- coding: utf8 -*-
__author__ = 'remy'

from Generation.views import render_conf_members, render_conf_hosts
from Generate_rules.manager import Manager
from django.shortcuts import render
from database.models import Hote, Membre

def generate_routeserver_conf(modeladmin, request, queryset):
    if modeladmin.model is Membre:
        data = render_conf_members(request, queryset)
        return render(request, "members_list.html", context=data)
    elif modeladmin.model is Hote:
        data = render_conf_hosts(request, queryset)
        return render(request, "members_list.html", context=data)

generate_routeserver_conf.short_description = "Générer la configuration BIRD pour la sélection"

def generate_openflow_rules(modeladmin, request, queryset):
    manager = Manager()
    manager.create_rules(queryset)
    modeladmin.message_user(request, "Les règles ont été mises à jour dans la base de données.")

generate_openflow_rules.short_description = "Générer la configuration Openflow pour la sélection"

def get_rules_list(modeladmin, request, queryset):
    text = ""
    for rule in queryset:
        text += rule.regle + "\n"
    return render(request, "switches_list.html", context={"rules": text})

get_rules_list.short_description = "Afficher une liste des règles sélectionnées"
