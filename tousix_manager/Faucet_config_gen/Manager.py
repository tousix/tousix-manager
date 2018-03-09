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


from tousix_manager.Database.models import Hote, Switchlink, Switch, Port
import yaml
from django.conf import settings

class Manager(object):
    def __init__(self):
        pass

# TODO implement link query for yaml script
    def generate_host(self, hote):

        hote = Hote.objects.get(id=1)
        cl = Host
        cl.name = hote.nomhote
        cl.location = hote.idport.idswitch.idpop.nompop
        cl.description = "Machine of member " + hote.idmembre.nommembre + ", location: " + cl.location
        cl.ipv4 = hote.ipv4hote
        cl.ipv6 = hote.ipv6hote
        cl.mac = hote.machote
        cl.port = hote.idport.numport

    def get_next_hop(self, node_src):
        pass

    def get_interfaces_switch(self, switch):
        pass

    def generate_datapath(self):
        result = {}
        for switch in Switch.objects.all():
            switch_def = {}
            switch_def['dp_id'] = switch.idswitch
            switch_def['hardware'] = switch.faucet_class
            intf = {}
            for port in Port.objects.filter(idswitch=switch.id):
                intf[port.numport] = {'acl_in': switch_def['dp_id'],
                                      'description': Hote.objects.filter(idport=port.id).get(0).nomhote,
                                      'name':  Hote.objects.filter(idport=port.id).get(0).nomhote,
                                      'native_vlan': settings['FAUCET_SETTINGS']['vlan_native_id'],
                                      'opstatus_reconf': False}
            switch_def['interfaces'] = intf
            result[switch.nomswitch] = switch_def
        return {'dps': result}
    def generate_acls(self):
        #TODO include script gen.py
        pass


class Interface(object):
    switch = 0xaaa
    port = 32
    name = "Port name"
    description = "Some port description"
    vlans = {"access": "access",
             "tagged": []}
    acls = []

    def gen_yaml(self):
        object = {self.port: {
            "name": self.name,
            "description": self.description,
            "acls_in": []
        }}
        if len(self.vlans['access']) ==1:
            object[self.port]['native_vlan'] = self.vlans["access"]
        if len(self.vlans['tagged']) >= 1:
            object[self.port]['tagged_vlans'] = self.vlans["tagged"]

        return yaml.dump(object)


class Host(object):

    name = ""
    ipv4 = ""
    ipv6 = ""
    mac = ""
    port = 3
    location = ""
    description = ""
