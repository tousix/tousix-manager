# -*- coding: utf8 -*-
__author__ = 'remy'
from django.db.models import Max
from django.utils.timezone import timedelta, now

from database.models import Flux, Stats

class forgeData(object):

    def get_data(self, source, destination, flux_type, period, unit):
        pk = self.get_flux_id(source, destination, flux_type)
        query = self.forge_query(pk, period)
        return self.forge_data(query, unit)

    def get_flux_id(self, source=0, destination=0, flux_type="IPv4"):

        query = Flux.objects.all()

        if flux_type == "ICMPv6" or flux_type == "ARP":
            query = query.filter(hote_src_id__isnull=True)
        elif source is not "0":
            query = query.filter(hote_src_id=source)

        if destination is not "0":
            query = query.filter(hote_dst_id=destination)

        query = query.filter(type=flux_type)
        liste_pk = query.values('idflux')
        return liste_pk

    def forge_query(self, pk, period='day'):
        liste_pk = []
        for primary in pk:
            liste_pk.append(primary.get('idflux'))
        query = Stats.objects.filter(idflux__in=liste_pk)

        if period == "hour":
            query = query.filter(time__gte=now() - timedelta(hours=1))
        elif period == "day":
            query = query.filter(time__gte=now() - timedelta(days=1))
        elif period == "month":
            query = query.filter(time__gte=now() - timedelta(days=31))
        elif period == "year":
            query = query.filter(time__gte=now() - timedelta(days=366))

        query = query.order_by("-time")

        query = query.values("time").annotate(bytes=Max('bytes'), packets=Max('packets'))
        return query

    def forge_data(self, stats, unit='bytes'):
        data_list = []
        for index, stat in list(enumerate(stats)):
            try:
                previous = stats[index + 1]
            except IndexError:
                break

            value = ((stat.get(unit) - previous.get(unit)) / self.diff_seconds(previous.get('time'), stat.get('time')))
            data = {'time': stat.get('time'),
                    'value': int(value)}
            data_list.append(data)
        return data_list

    def diff_seconds(self, datetime1, datetime2):
        if datetime2 >= datetime1:
            time_diff = datetime2 - datetime1
        else:
            time_diff = datetime1 - datetime2
        return time_diff.total_seconds()
