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
        render_ipv4 = render(self.request, "ipv4.conf", context={"peers": peers})
        render_ipv6 = render(self.request, "ipv6.conf", context={"peers": peers})
        return render(self.request, "members_list.html", context={"ipv4": render_ipv4.content,
                                                                  "ipv6": render_ipv6.content})
