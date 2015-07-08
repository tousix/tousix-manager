# -*- coding: utf8 -*-
__author__ = 'remy'

import logging
from database.models import Flux, Stats
from django.utils.timezone import now

LOG = logging.getLogger("Logging_stats")

class FlowProcess(object):
    def decodeRequest(self, request):
        datas = []
        for key, value in request.items():
            LOG.info("Stats recieved from : " + key)
            # TODO Verify if switch is in the database

            for stat in value:
                data = {"dpid": key}
                self.decode_flux(data, stat)
                self.decode_data(data, stat)
                datas.append(data)
        self.save_stat(datas)

    def decode_data(self, data, stat):
        data['bytes'] = stat.get('byte_count')
        data['packets'] = stat.get('packet_count')

    def decode_flux(self, data, stat):
        cookie = stat.get('cookie')
        source = (cookie >> 32) - 1024
        destination = (cookie & 0x00000000FFFFFFFF) - 1024
        type = self.guess_flux_type(stat)
        flux_id = self.get_flux_id(source, destination, type)
        data['flux'] = flux_id

    def get_flux_id(self, source=0, destination=0, flux_type="IPv4"):

        query = Flux.objects.all()

        if flux_type == "ICMPv6" or flux_type == "ARP":
            query = query.filter(hote_src_id__isnull=True)
        elif source is not "0":
            query = query.filter(hote_src_id=source)

        if destination is not "0":
            query = query.filter(hote_dst_id=destination)

        query = query.filter(type=flux_type)
        pk = query.values('idflux').first()
        return pk.get('idflux')

    def guess_flux_type(self, stat):
        match = stat.get('match')
        if match.get("dl_type") == 2054:
            return "ARP"
        elif match.get("dl_type") == 2048:
            return "IPv4"
        elif match.get("dl_type") == 34525:
            if "ipv6_src" in match:
                return "IPv6"
            else:
                return "ICMPv6"

    def save_stat(self, datas):
        time = now()
        stats = []
        for data in datas:
            stats.append(Stats(time=time, bytes=data.get('bytes'), packets=data.get('packets'), idflux_id=data.get('flux')))
        Stats.objects.bulk_create(stats)
