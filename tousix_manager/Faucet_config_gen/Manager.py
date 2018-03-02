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


from tousix_manager.Database.models import Hote, Vlan, Hote_VLAN
import yaml


class Manager(object):
    def __init__(self):
        pass

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

    def generate_all_peers(self):
        hotes = Hote.objects.filter(valid=True).exclude(etat="Inactive")
        yaml_interfaces = []
        for host in hotes:
            yaml_interfaces.append(self.generate_peer(host))

        return yaml_interfaces

    def generate_peer(self, member):
        member = Hote.objects.filter(valid=True).exclude(etat="Inactive").get(id=1)
        interface = Interface()
        interface.port = member.port()
        interface.switch = member.idport.idswitch
        interface.name = member.nomhote
        interface.description = "Member " + member.idmembre.nommembre + ": " + member.nomhote
        interface.vlans['access'].extend(Hote_VLAN.objects.filter(hote=member, mode=False).all().values('vlan__vlan_id'))
        interface.vlans['tagged'].extend(Hote_VLAN.objects.filter(hote=member, mode=True).all().values('vlan__vlan_id'))

        interface.acls = []

        return interface.gen_yaml()


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
