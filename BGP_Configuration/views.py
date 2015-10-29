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

from django.views.generic.edit import FormView
from django.shortcuts import render, render_to_response

from BGP_Configuration.forms import MembersChoiceForm
from Database.models import Hote

from django.conf import settings
import logging
from BGP_Configuration.birdlg import bird_proxy

LOG = logging.getLogger("BGP_Configuration")


class SelectionMemberView(FormView):
    """
    This view is only used for testing purposes.
    You can go to the admin panel to use this app.
    """
    form_class = MembersChoiceForm
    template_name = "members_list.html"

    def form_valid(self, form):
        members = form.get_selected().filter(approved=True)
        data = render_conf_members(members)
        return render(self.request, "members_list.html", context=data)


def render_conf_members(members):
    """
    Render the BIRD config files with the members selected
    :param members: List of member model objects
    :return:
    """
    peers = []

    for member in members:
        query = Hote.objects.filter(idmembre=member.pk)
        for host in query:
            peer = {"member": member.nommembre,
                    "mac": host.machote,
                    "ipv4": host.ipv4hote,
                    "ipv6": host.ipv6hote,
                    'peer': host.nomhote,
                    "as": member.asnumber}
            peers.append(peer)
    render_ipv4 = render_to_response("ipv4.conf", context={"peers": peers})
    render_ipv6 = render_to_response("ipv6.conf", context={"peers": peers})
    send_bgp_config(render_ipv4.content, render_ipv6.content)
    results = reload_bgp_config()
    return {"ipv4": results,
            "ipv6": results}


def render_conf_hosts(hosts):
    """
    Render the BIRD config files with the hosts selected
    :param hosts: List of hosts model objects
    :return:
    """
    peers = []
    for host in hosts:
        peer = {"member": host.idmembre.nommembre,
                "mac": host.machote,
                "ipv4": host.ipv4hote,
                "ipv6": host.ipv6hote,
                'peer': host.nomhote,
                "as": host.idmembre.asnumber}
        peers.append(peer)
    render_ipv4 = render_to_response("ipv4.conf", context={"peers": peers})
    render_ipv6 = render_to_response("ipv6.conf", context={"peers": peers})

    send_bgp_config(render_ipv4.content, render_ipv6.content)
    results = reload_bgp_config()
    return {"ipv4": results,
            "ipv6": results}


def send_bgp_config(config_ipv4, config_ipv6):
    # rewrite bgp configuration file
    for server in settings.BGP_CONFIG:
        write_config_file(server["filepath"], config_ipv4)
        write_config_file(server["filepath6"], config_ipv6)


def write_config_file(filepath, config_file):
    try:
        file = open(filepath, mode="wb")
    except OSError:
        LOG.error("Error when trying to access the file.")
        return
    file.write(config_file)
    file.close()


def reload_bgp_config():
    results = []
    for server in settings.BGP_CONFIG:
        reload_ipv4 = bird_proxy(server["host"], server["port"], "ipv4", "bird", "configure")
        if reload_ipv4[0] is False:
            LOG.error(reload_ipv4[1])
        else:
            results.append({server["name"] + "_ipv4": reload_ipv4[1]})
        reload_ipv6 = bird_proxy(server["host"], server["port"], "ipv6", "bird", "configure")
        if reload_ipv6[0] is False:
            LOG.error(reload_ipv6[1])
        else:
            results.append({server["name"] + "_ipv6": reload_ipv6[1]})
    return results
