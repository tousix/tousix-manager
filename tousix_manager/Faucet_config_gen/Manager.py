#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2018 Marc Bruyere <mbruyere ad nc dot u-tokyo dot ac dot jp>
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
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as qs
from django.conf import settings
yaml = YAML()


def HexInt(i):
    ''' function to insert right hexa dpids '''
    stri = "0x" + hex(i)[2:].upper().zfill(1)

    return yaml.load(stri)


def Braket(i):
    ''' function to remove the brackets for the Groupe faiover buckets'''

    return yaml.load(i)

class Manager(object):
    def __init__(self):
        self.faucet_settings = settings.FAUCET_SETTINGS
        self.data = ()

    def convert_table(self):
        list = []
        for host in Hote.objects.all():
            table = {"idrtr": host.idhote,
                     "hostname": host.nomhote,
                     "addr_ipv4": host.ipv4hote,
                     "addr_ipv6": host.ipv6hote,
                     "macaddr": host.machote,
                     "membre": host.idmembre.nommembre,
                     "pop": host.pop(),
                     "switch": host.switch(),
                     'port': host.idport.numport,
                     "status": host.etat}
            list.append(table)

        return list


    def triangle(self, list_load = []):


        data = {'vlans': {Switch.objects.get(nomswitch="Edge 1").nomswitch: {'vid': 101, 'description': qs(self.faucet_settings['vlan_name']), 'acl_in': 1},
                          Switch.objects.get(nomswitch="Edge 2").nomswitch: {'vid': 102, 'description': qs(self.faucet_settings['vlan_name']), 'acl_in': 2},
                          Switch.objects.get(nomswitch="Edge 3").nomswitch: {'vid': 103, 'description': qs(self.faucet_settings['vlan_name']), 'acl_in': 3}},
                'dps': {Switch.objects.get(nomswitch="Edge 1").nomswitch: {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge 1").dpid_switch), 'hardware': qs(Switch.objects.get(nomswitch="Edge 1").faucet_class), 'interfaces': {
                    int(self.faucet_settings['sw1_portnum_to_sw2']): {'name': qs('Uplink'), 'description': qs('link_sw1_sw2'),
                                              'native_vlan': Switch.objects.get(nomswitch="Edge 1").nomswitch, 'opstatus_reconf': False},
                    int(self.faucet_settings['sw1_portnum_to_sw3']): {'name': qs('Uplink'), 'description': qs('link_sw1_sw3'),
                                              'native_vlan': Switch.objects.get(nomswitch="Edge 1").nomswitch, 'opstatus_reconf': False}}},
                        Switch.objects.get(nomswitch="Edge 2").nomswitch: {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge 2").dpid_switch), 'hardware': qs(Switch.objects.get(nomswitch="Edge 2").faucet_class), 'interfaces': {
                            int(self.faucet_settings['sw2_portnum_to_sw1']): {'name': qs('Uplink'), 'description': qs('link_sw2_sw1'),
                                                      'native_vlan': Switch.objects.get(nomswitch="Edge 2").nomswitch, 'opstatus_reconf': False},
                            int(self.faucet_settings['sw2_portnum_to_sw3']): {'name': qs('Uplink'), 'description': qs('link_sw2_sw3'),
                                                      'native_vlan': Switch.objects.get(nomswitch="Edge 2").nomswitch, 'opstatus_reconf': False}}},
                        Switch.objects.get(nomswitch="Edge 3").nomswitch: {'dp_id': HexInt(Switch.objects.get(nomswitch="Edge 3").dpid_switch), 'hardware': qs(Switch.objects.get(nomswitch="Edge 3").faucet_class), 'interfaces': {
                            int(self.faucet_settings['sw3_portnum_to_sw1']): {'name': qs('Uplink'), 'description': qs('link_sw3_sw1'),
                                                      'native_vlan': Switch.objects.get(nomswitch="Edge 3").nomswitch, 'opstatus_reconf': False},
                            int(self.faucet_settings['sw3_portnum_to_sw2']): {'name': qs('Uplink'), 'description': qs('link_sw3_sw2'),
                                                      'native_vlan': Switch.objects.get(nomswitch="Edge 3").nomswitch, 'opstatus_reconf': False}}}},
                'acls': {1: [],
                         2: [],
                         3: []}}

        for i in range(len(list_load)):
            if list_load[i]['switch'] == Switch.objects.get(nomswitch="Edge 1").nomswitch and list_load[i]['status'] == 'Production':
                data['dps'][Switch.objects.get(nomswitch="Edge 1").nomswitch]['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                  'description': qs(
                                                                                      list_load[i]['hostname']),
                                                                                  'native_vlan': Switch.objects.get(nomswitch="Edge 1").nomswitch}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][1].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']),
                                  'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})

                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']),
                              'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 1 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw2_portnum_to_sw1'] + ',' + self.faucet_settings['sw2_portnum_to_sw3'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][2].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 100 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw2_portnum_to_sw1'] + ',' + self.faucet_settings['sw2_portnum_to_sw3'] + ']')}}}}})

                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 200 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw2_portnum_to_sw1'] + ',' + self.faucet_settings['sw2_portnum_to_sw3'] + ']')}}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 300 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw3_portnum_to_sw1'] + ',' + self.faucet_settings['sw3_portnum_to_sw2'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][3].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 400 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw3_portnum_to_sw1'] + ',' + self.faucet_settings['sw3_portnum_to_sw2'] + ']')}}}}})

                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 500 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw3_portnum_to_sw1'] + ',' + self.faucet_settings['sw3_portnum_to_sw2'] + ']')}}}}})

            elif list_load[i]['switch'] == Switch.objects.get(nomswitch="Edge 2").nomswitch and list_load[i]['status'] == 'Production':
                data['dps'][Switch.objects.get(nomswitch="Edge 2").nomswitch]['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                  'description': qs(
                                                                                      list_load[i]['hostname']),
                                                                                  'native_vlan': Switch.objects.get(nomswitch="Edge 2").nomswitch}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 600 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw1_portnum_to_sw2'] + ',' + self.faucet_settings['sw1_portnum_to_sw3'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][1].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 700 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw1_portnum_to_sw2'] + ',' + self.faucet_settings['sw1_portnum_to_sw3'] + ']')}}}}})

                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 800 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw1_portnum_to_sw2'] + ',' + self.faucet_settings['sw1_portnum_to_sw3'] + ']')}}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][2].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']),
                                  'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})

                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']),
                              'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 900 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw3_portnum_to_sw2'] + ',' + self.faucet_settings['sw3_portnum_to_sw1'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][3].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 1000 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw3_portnum_to_sw2'] + ',' + self.faucet_settings['sw3_portnum_to_sw1'] + ']')}}}}})

                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 1100 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw3_portnum_to_sw2'] + ',' + self.faucet_settings['sw3_portnum_to_sw1'] + ']')}}}}})

            elif list_load[i]['switch'] == Switch.objects.get(nomswitch="Edge 3").nomswitch and list_load[i]['status'] == 'Production':
                data['dps'][Switch.objects.get(nomswitch="Edge 3").nomswitch]['interfaces'][int(list_load[i]['port'])] = {'name': qs(list_load[i]['hostname']),
                                                                                  'description': qs(
                                                                                      list_load[i]['hostname']),
                                                                                  'native_vlan': Switch.objects.get(nomswitch="Edge 3").nomswitch}
                data['acls'][1].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 1200 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw1_portnum_to_sw3'] + ',' + self.faucet_settings['sw1_portnum_to_sw2'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][1].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 1300 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw1_portnum_to_sw3'] + ',' + self.faucet_settings['sw1_portnum_to_sw2'] + ']')}}}}})

                data['acls'][1].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 1400 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw1_portnum_to_sw3'] + ',' + self.faucet_settings['sw1_portnum_to_sw2'] + ']')}}}}})

                data['acls'][2].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'failover': {'group_id': 1500 + i, 'ports': Braket(
                        '[' + self.faucet_settings['sw2_portnum_to_sw3'] + ',' + self.faucet_settings['sw2_portnum_to_sw1'] + ']')}}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][2].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']), 'actions': {'output': {'pop_vlans': True,
                                                                               'failover': {'group_id': 1600 + i,
                                                                                            'ports': Braket(
                                                                                                '[' + self.faucet_settings['sw2_portnum_to_sw3'] + ',' + self.faucet_settings['sw2_portnum_to_sw1'] + ']')}}}}})

                data['acls'][2].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']), 'actions': {'output': {'pop_vlans': True,
                                                                           'failover': {'group_id': 1700 + i,
                                                                                        'ports': Braket(
                                                                                            '[' + self.faucet_settings['sw2_portnum_to_sw3'] + ',' + self.faucet_settings['sw2_portnum_to_sw1'] + ']')}}}}})

                data['acls'][3].append({'rule': {'dl_dst': qs(list_load[i]['macaddr']), 'actions': {
                    'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})
                if self.faucet_settings['IPV6_active'] == True:
                    data['acls'][3].append(
                        {'rule': {'dl_type': HexInt(0x86dd), 'ip_proto': 58, 'icmpv6_type': 135, 'ipv6_nd_target': qs(
                            list_load[i]['addr_ipv6']),
                                  'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})

                data['acls'][3].append(
                    {'rule': {'dl_type': HexInt(0x806), 'dl_dst': qs('ff:ff:ff:ff:ff:ff'), 'arp_tpa': qs(
                        list_load[i]['addr_ipv4']),
                              'actions': {'output': {'pop_vlans': True, 'port': int(list_load[i]['port'])}}}})
        data['acls'][1].append({'rule': {'actions': {'allow': 0}}})
        data['acls'][2].append({'rule': {'actions': {'allow': 0}}})
        data['acls'][3].append({'rule': {'actions': {'allow': 0}}})
        return (data)

    def generate_all_peers(self):
        self.data = self.triangle(self.convert_table())
        return self.data

    def dump_config(self):
        if len(self.data) is not 0:
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.indent = 40
            yaml.preserve_quotes = True
            yaml.boolean_representation = ['False', 'True']
            yaml.default_flow_style = False

            yaml.dump(self.data, open(self.faucet_settings['faucet_config_path'],'w'))

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
