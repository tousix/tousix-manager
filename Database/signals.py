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

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from Database.models import Hote, Flux, Stats
from BGP_Configuration.views import render_conf_hosts
from django.db.models import Q
from Rules_Deployment.rules import RulesDeployment


@receiver(post_save, sender=Hote)
def post_save_hote(sender, **kwargs):
    """
    Signal used for creating flux objects in the Database (for statistic purposes)
    :param sender:
    :param kwargs:
    :return:
    """
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

