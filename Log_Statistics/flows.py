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

import logging
from Database.models import Flux, Stats, Switch
from django.utils.datetime_safe import datetime

LOG = logging.getLogger("Log_Statistics")


class FlowProcess(object):
    """
    Class for flow statistics processing and commit.
    """
    def decode_request(self, request, time):
        datas = []
        for key, value in request.items():
            LOG.info("Stats recieved from : " + key)

            # Verify if the switch is in the Database
            if Switch.objects.filter(pk=key).exists():
                for stat in value:
                    data = {"dpid": key}
                    if self.decode_flow(data, stat) is None:
                        self.decode_data(data, stat)
                        datas.append(data)
            self.save_stat(datas, datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f"))

    def decode_data(self, data, stat):
        data['bytes'] = stat.get('byte_count')
        data['packets'] = stat.get('packet_count')

    def decode_flow(self, data, stat):
        """
        Retrieve flow information form cookie.
        :param data: flow stat data output
        :param stat: flow stat send by the controller
        :return:
        """
        cookie = stat.get('cookie')
        source = (cookie >> 32) - 1024
        if source < 0:
            return "IGNORE"
        destination = (cookie & 0x00000000FFFFFFFF) - 1024
        if destination < 0:
            return "IGNORE"
        type = self.guess_flow_type(stat)
        flow_id = self.get_flow_id(source, destination, type)
        if flow_id is None:
            return "IGNORE"
        data['flow'] = flow_id
        return None

    def get_flow_id(self, source=0, destination=0, flow_type="IPv4"):
        """
        Retrieve flow id from the Database.
        :param source: source host ID
        :param destination: destination host ID
        :param flow_type: flow type
        :return:
        """
        query = Flux.objects.all()

        if flow_type == "ICMPv6" or flow_type == "ARP":
            query = query.filter(hote_src_id__isnull=True)
        elif source is not 0:
            query = query.filter(hote_src_id=source)

        if destination is not 0:
            query = query.filter(hote_dst_id=destination)

        query = query.filter(type=flow_type)
        pk = query.values('idflux').first()
        try:

            return pk.get('idflux')
        except AttributeError:
            return None

    def guess_flow_type(self, stat):
        """
        Guess flow type based on dl_type match component in the flow statistic.
        :param stat: flow statistic
        :return: flow_type
        """
        match = stat.get('match')
        if match.get("dl_type") == 2054:
            return "ARP"
        elif match.get("dl_type") == 2048:
            return "IPv4"
        elif match.get("dl_type") == 34525:
            if "icmpv6_type" not in match:
                return "IPv6"
            else:
                return "ICMPv6"

    def save_stat(self, datas, time):
        """
        Save statistics into the Database.
        :param datas:
        :return:
        """
        stats = []
        for data in datas:
            stats.append(Stats(time=time, bytes=data.get('bytes'), packets=data.get('packets'),
                               idflux_id=data.get('flow'), idswitch_id=data.get("dpid")))
        Stats.objects.bulk_create(stats)
