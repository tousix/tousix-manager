# -*- coding: utf8 -*-
__author__ = 'remy'

from Rules_Generation.Production.Dataflow.manager import Manager as Dataflow
from Rules_Generation.Production.Umbrella.manager import Manager as Umbrella
from Rules_Generation.configuration import configuration as conf

class Manager(object):
    """
    Manager class for creating production rules.
    """
    def create_rules_members(self, dpid, peers):
        """
        Create all the production rules needed for the members.
        :param dpid: Target DPID
        :type dpid: int
        :param members: Peer object array
        :type members: list(Peer)
        :return: flows rules array
        """
        rules = []
        dataflow = Dataflow()
        umbrella = Umbrella()
        for peer in peers:
            if conf.enabled["Production"].get('Dataflow') is True:
                rules.extend(dataflow.create_rules(dpid, peer))
            if (conf.enabled["Production"].get('Umbrella').get('IPv4') |
                    conf.enabled["Production"].get('Umbrella').get('IPv6')) is True:
                rules.extend(umbrella.create_rules(dpid, peer))
        return rules
