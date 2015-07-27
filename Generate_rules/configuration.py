# -*- coding: utf8 -*-
__author__ = 'remy'


class configuration(object):
    """
    This class is intended for replacing the configuration file of the original program.
    It contains all the parameters needed for the exectution of the application.
    """
    enabled = {
        "Production": {
           "Umbrella": {
               "IPv4": True,
               "IPv6": True
           },
           "Dataflow": True
        },

        "Stats": {
            "IPv4": True,
            "IPv6": True,
            "ICMPv6": True,
            "ARP": True
        }
    }
    priority = {
                "Production": {
           "Umbrella": {
               "IPv4": 1000,
               "IPv6": 900
           },
           "Dataflow": 1000
        },

        "Stats": {
            "IPv4": 1000,
            "IPv6": 1000,
            "ICMPv6": 1000,
            "ARP": 1000
        }
    }
    groups = {2221123978211977908: 1,
              10925425496585651080: 3,
              16690345156023249453: 2
              }
class Peer(object):
    """
    Defines peer object
    """

    Egress = True
    IPv4 = "127.0.0.1"
    IPv6 = "fe80::1"
    Mac = "00:00:00:00:00:00"
    Name = "DefaultPeer"
    idPeer = 0
    nextHop = 5149618658
    outputPort = 32
