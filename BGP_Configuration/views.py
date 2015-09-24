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
from django.shortcuts import render

from BGP_Configuration.forms import MembersChoiceForm
from Database.models import Hote


class SelectionMemberView(FormView):
    """
    This view is only used for testing purposes.
    You can go to the admin panel to use this app.
    """
    form_class = MembersChoiceForm
    template_name = "members_list.html"

    def form_valid(self, form):
        members = form.get_selected().filter(approved=True)
        data = render_conf_members(self.request, members)
        return render(self.request, "members_list.html", context=data)


def render_conf_members(request, members):
    """
    Render the BIRD config files with the members selected
    :param request: HTTP request
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
    render_ipv4 = render(request, "ipv4.conf", context={"peers": peers})
    render_ipv6 = render(request, "ipv6.conf", context={"peers": peers})
    return {"ipv4": render_ipv4.content,
            "ipv6": render_ipv6.content}


def render_conf_hosts(request, hosts):
    """
    Render the BIRD config files with the hosts selected
    :param request: HTTP request
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
    render_ipv4 = render(request, "ipv4.conf", context={"peers": peers})
    render_ipv6 = render(request, "ipv6.conf", context={"peers": peers})
    return {"ipv4": render_ipv4.content,
            "ipv6": render_ipv6.content}
