# -*- coding: utf8 -*-
__author__ = 'remy'

from Generation.views import render_conf_members, render_conf_hosts
from Generate_rules.manager import Manager
from django.shortcuts import render, redirect
from database.models import Hote, Membre
from Deployment.views import RulesDeploymentConfirmView

def generate_routeserver_conf(modeladmin, request, queryset):
    """
    Action for generating BIRD configuration files.
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    # remove keyboard-chair errors
    if modeladmin.model is Membre:
        queryset = queryset.exclude(nommembre="TouIX")
        data = render_conf_members(request, queryset)
        return render(request, "members_list.html", context=data)
    elif modeladmin.model is Hote:
        queryset = queryset.exclude(idmembre__nommembre="TouIX")
        data = render_conf_hosts(request, queryset)
        return render(request, "members_list.html", context=data)

generate_routeserver_conf.short_description = "Générer la configuration BIRD pour la sélection"


def generate_openflow_rules(modeladmin, request, queryset):
    """
    Action for generating openflow rules on switch.
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    manager = Manager()
    manager.create_rules(queryset)
    modeladmin.message_user(request, "Les règles ont été mises à jour dans la base de données.")
    return redirect('rules_confirm')

generate_openflow_rules.short_description = "Générer la configuration Openflow pour la sélection"


def get_rules_list(modeladmin, request, queryset):
    """
    Action for display plain text rules selected in admin view.
    """
    text = ""
    for rule in queryset:
        text += rule.regle + "\n"
    return render(request, "switches_list.html", context={"rules": text})

get_rules_list.short_description = "Afficher une liste des règles sélectionnées"


def change_hote_status(modeladmin, request, queryset):
    """
    This action is only present because the change status button
    of an django application does not seem to work (django-fsm-admin).
    """
    for hote in queryset:
        if hote.etat == "Changing":
            hote.Apply()
            hote.save()
            modeladmin.message_user(request, "Le statut du routeur "+hote.nomhote+" a été changé.")
        elif hote.etat == "Inactive":
            hote.Deploy()
            hote.save()
            modeladmin.message_user(request, "Le statut du routeur "+hote.nomhote+" a été changé.")

change_hote_status.short_description = "Changer le statut des routeurs sélectionnées"