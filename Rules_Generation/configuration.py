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


class configuration(object):
    """
    This class is intended for replacing the configuration file of the original program.
    It contains all the parameters needed for the exectution of the application.
    """
    enabled = {
        "Production": {
           "Umbrella": {
               "IPv4": True,
               "IPv6": False
           },
           "Dataflow": True
        },

        "Stats": {
            "IPv4": True,
            "IPv6": False,
            "ICMPv6": False,
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
