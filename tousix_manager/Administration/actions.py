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
from tousix_manager.Database.models import Hote, Membre, Switch
from tousix_manager.Rules_Generation.manager import Manager as RyuManager
from tousix_manager.Faucet_config_gen.Manager import Manager as FaucetManager
from tousix_manager.Rules_Deployment.rules import RulesDeployment
from tousix_manager.Statistics_Manager.billing_influx import BillingView
import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

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
        data = render_conf_members(queryset)
        return render(request, "members_list.html", context=data)
    elif modeladmin.model is Hote:
        queryset = queryset.exclude(idmembre__nommembre="TouIX")
        data = render_conf_hosts(queryset)
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
    manager = RyuManager()
    manager.create_rules(queryset)
    modeladmin.message_user(request, "Les règles ont été mises à jour dans la base de données.")
    return redirect('rules_confirm')

generate_openflow_rules.short_description = "Générer la configuration Openflow pour la sélection sur un contrôleur Ryu"


def generate_faucet_config(modeladmin, request, queryset):
    """
    Action for generating openflow rules on switch.
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    manager = FaucetManager()
    data = manager.generate_all_peers()
    manager.dump_config()
    modeladmin.message_user(request, "Le fichier de configuration Faucet a été modifié. Veuillez recharger le service afin d'appliquer les modifications")
    return render(request, "config_confirm.html", context={"data": data})

generate_faucet_config.short_description = "Générer la configuration Faucet tous les hôtes"


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


def apply_hote_on_production(modeladmin, request, queryset):
    """
    Action to apply openflow flow rules from selected hosts into the controller.
    """
    for hote in queryset:
        if hote.valid is True:
            manager = Manager()
            manager.create_rules_single(Switch.objects.all(), hote)
            deployment = RulesDeployment()
            deployment.send_flowrules_single_host(Switch.objects.all(), hote)
            modeladmin.message_user(request, "Les paramètres du router "+hote.nomhote+" ont été appliqués sur la production.")
        else:
            raise Exception("Not a valid router.")

apply_hote_on_production.short_description = "Appliquer les changements des hôtes sur la production"


def get_percentile_hote(modeladmin, request, queryset):
    billing = BillingView()
    for hote in queryset:
        modeladmin.message_user(request, "Bande passante consommé pour l'hôte " + hote.nomhote + ": " + str(billing.show_result(hote.idhote)) + " bit/s")

get_percentile_hote.short_description = "Afficher l'utilisation de la bande passante au courcs  de l'année (95 centile)"

def download_csv(modeladmin, request, queryset):
    """
    Snippet from https://djangosnippets.org/snippets/2690/
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
download_csv.short_description = "Download selected as csv"

def download_csv_faucet(modeladmin, request, queryset):
    """
    Snippet from https://djangosnippets.org/snippets/2690/
    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = queryset.model._meta
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = ["idrtr", "hostname", "addr_ipv4", "addr_ipv6", "macaddr", "membre", "pop", "switch", "port", "status"]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([obj.idhote, obj.nomhote, obj.addr_ipv4, obj.addr_ipv6, obj.macaddr, obj.membre, obj.pop, obj.switch, obj.port, obj.etat])
    return response
download_csv_faucet.short_description = "Download selected as csv for faucet configuration"