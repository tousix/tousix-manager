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

from django.db.models import Q
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from tousix_manager.BGP_Configuration.views import render_conf_hosts
from tousix_manager.Database.models import Hote, Flux, Stats, Switch
from tousix_manager.Rules_Deployment.rules import RulesDeployment
from tousix_manager.Rules_Generation.manager import Manager


@receiver(post_save, sender=Hote)
def post_save_hote_creation(sender, **kwargs):
    """
    Signal used for creating flux objects in the Database (for statistic purposes)
    :param sender:
    :param kwargs:
    :return:
    """
    if not kwargs.get('raw', False):
        if kwargs['created'] is True:
            db_flux = list()
            db_flux.append(Flux(hote_src=None, hote_dst=kwargs['instance'], type="ICMPv6"))
            db_flux.append(Flux(hote_src=None, hote_dst=kwargs['instance'], type="ARP"))
            for peer_dst in Hote.objects.all():
                if peer_dst != kwargs['instance']:
                    db_flux.append(Flux(hote_src=peer_dst, hote_dst=kwargs['instance'], type="IPv4"))
                    db_flux.append(Flux(hote_src=kwargs['instance'], hote_dst=peer_dst, type="IPv4"))
                    db_flux.append(Flux(hote_src=peer_dst, hote_dst=kwargs['instance'], type="IPv6"))
                    db_flux.append(Flux(hote_src=kwargs['instance'], hote_dst=peer_dst, type="IPv6"))
            Flux.objects.bulk_create(db_flux)

            # Deploy BGP configuration with the new host
            render_conf_hosts(Hote.objects.all())


@receiver(pre_save, sender=Hote)
def pre_save_hote_modification(sender, **kwargs):
    """
    Signal to enforce modifications on topology for some fields modified in Hote.
    Actions coded:
    - Modfiy IP(v4 and v6) informations on topology
    :param sender:
    :param kwargs:
    :return:
    """
    if not kwargs.get('raw', False):
        instance = kwargs['instance']
        try:
            previous_hote = Hote.objects.get(pk=instance.pk)
        except Hote.DoesNotExist:
            # skip this step if new object
            return None
        if previous_hote.ipv6hote != instance.ipv6hote or previous_hote.ipv6hote != previous_hote.ipv4hote:
            conflict_ip = Hote.objects.filter(Q(ipv4hote=instance.ipv4hote) | Q(ipv6hote=instance.ipv6hote))
            if conflict_ip.count() is not 0:
                error_string = "IP address is already assigned to these hosts: "
                for host_conflict in conflict_ip:
                    error_string += host_conflict.nomhote + ", "
                raise ValidationError(error_string)

            manager = Manager()
            manager.create_rules_single(Switch.objects.all(), instance)
            deployment = RulesDeployment()
            deployment.send_flowrules_single_host(Switch.objects.all(), instance)


@receiver(pre_delete, sender=Hote)
def pre_delete_hote(sender, **kwargs):
    """
    Clean-up all traces of the router in the Database.
    :param sender:
    :param kwargs:
    :return:
    """
    # Retrieve all flux where the deleted host is present
    flux_list = Flux.objects.filter(Q(hote_src=kwargs['instance']) | Q(hote_dst=kwargs['instance']))
    # Remove stats from these flux
    Stats.objects.filter(idflux__in=flux_list).delete()
    # delete flux
    flux_list.delete()

    # remove rules for designated host
    deployment = RulesDeployment()
    deployment.remove_host([kwargs['instance']])

    # Remove host from the BGP configuration
    render_conf_hosts(Hote.objects.exclude(idhote=kwargs['instance'].idhote))

