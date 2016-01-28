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

from django.shortcuts import render, redirect
from tousix_manager.BGP_Configuration.views import render_conf_members, render_conf_hosts
from tousix_manager.Database.models import Hote, Membre
from tousix_manager.Rules_Generation.manager import Manager


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