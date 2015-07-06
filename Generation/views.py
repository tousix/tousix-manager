# -*- coding: utf8 -*-
__author__ = 'remy'

from django.views.generic.edit import FormView
from django.shortcuts import render

from Generation.forms import MembersChoiceForm
from database.models import Hote


class SelectionMemberView(FormView):
    form_class = MembersChoiceForm
    template_name = "members_list.html"

    def form_valid(self, form):
        members = form.get_selected()
        data = render_conf_members(self.request, members)
        return render(self.request, "members_list.html", context=data)

def render_conf_members(request, members):
    peers = []

    for member in members:
        query = Hote.objects.filter(idmembre=member.pk).values('machote', 'ipv4hote', 'ipv6hote', 'nomhote')
        for host in query:
            peer = {"member": member.nommembre,
                    "mac": host.get('machote'),
                    "ipv4": host.get('ipv4hote'),
                    "ipv6": host.get('ipv6hote'),
                    'peer': host.get('nomhote'),
                    "as": member.asnumber}
            peers.append(peer)
    render_ipv4 = render(request, "ipv4.conf", context={"peers": peers})
    render_ipv6 = render(request, "ipv6.conf", context={"peers": peers})
    return {"ipv4": render_ipv4.content,
            "ipv6": render_ipv6.content}

def render_conf_hosts(request, hosts):
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
