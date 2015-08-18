# -*- coding: utf8 -*-
__author__ = 'remy'

import logging
from database.models import Flux, Stats, Switch
from django.utils.timezone import now

LOG = logging.getLogger("Logging_stats")


class FlowProcess(object):
    """
    Class for flow statistics processing and commit.
    """
    def decode_request(self, request):
        datas = []
        for key, value in request.items():
            LOG.info("Stats recieved from : " + key)

            # Verify if the switch is in the database
            if Switch.objects.filter(pk=key).exists():
                for stat in value:
                    data = {"dpid": key}
                    self.decode_flow(data, stat)
                    self.decode_data(data, stat)
                    datas.append(data)
            self.save_stat(datas)

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
        destination = (cookie & 0x00000000FFFFFFFF) - 1024
        type = self.guess_flow_type(stat)
        flow_id = self.get_flow_id(source, destination, type)
        data['flow'] = flow_id

    def get_flow_id(self, source=0, destination=0, flow_type="IPv4"):
        """
        Retrieve flow id from the database.
        :param source: source host ID
        :param destination: destination host ID
        :param flow_type: flow type
        :return:
        """
        query = Flux.objects.all()

        if flow_type == "ICMPv6" or flow_type == "ARP":
            query = query.filter(hote_src_id__isnull=True)
        elif source is not "0":
            query = query.filter(hote_src_id=source)

        if destination is not "0":
            query = query.filter(hote_dst_id=destination)

        query = query.filter(type=flow_type)
        pk = query.values('idflux').first()
        return pk.get('idflux')

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

    def save_stat(self, datas):
        """
        Save statistics into the database.
        :param datas:
        :return:
        """
        stats = []
        time = now()
        for data in datas:
            stats.append(Stats(time=time, bytes=data.get('bytes'), packets=data.get('packets'),
                               idflux_id=data.get('flow'), idswitch_id=data.get("dpid")))
        Stats.objects.bulk_create(stats)
