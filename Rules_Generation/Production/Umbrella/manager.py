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


from Rules_Generation.Production.Umbrella.ipv4 import IPv4
from Rules_Generation.Production.Umbrella.ipv6 import IPv6
from Rules_Generation.configuration import configuration as conf
from django.conf import settings

class Manager(object):
    """
    Manager class for creating Umbrella rules.
    """
    def create_rules(self, dpid, peer):
        """
        Create Umbrella rules.
        :param dpid: Target DPID
        :type dpid: int
        :param member: Peer object
        :type member: Peer
        :return: Flow rules array
        """
        ipv6 = IPv6()
        ipv4 = IPv4()
        rules = []
        enabled = settings.RULES_GENERATION_ENABLED
        if (enabled["Production"].get('Umbrella').get('IPv6')) is True:
            rule = {"module": "Production_Umbrella_IPv6",
                    "rule": ipv6.create_umbrella(dpid, peer),
                    "source": None,
                    "destination": peer.idPeer}
            rules.append(rule)
        if (enabled["Production"].get('Umbrella').get('IPv4')) is True:
            rule = {"module": "Production_Umbrella_IPv4",
                    "rule": ipv4.create_umbrella(dpid, peer),
                    "source": None,
                    "destination": peer.idPeer}
            rules.append(rule)
        return rules
