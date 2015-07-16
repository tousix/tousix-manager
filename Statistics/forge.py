# -*- coding: utf8 -*-
__author__ = 'remy'
from django.db.models import Sum
from django.utils.timezone import timedelta, now

from database.models import Flux, Stats, Switch

class forgeData(object):

    probe_time_interval = 5
    time_first_value = now()

    def get_data(self, source, destination, flux_type, period, unit):
        self.now = now()
        pk = self.get_flux_id(source, destination, flux_type)
        switches = Switch.objects.all()
        datas_non_aggregated = []
        for switch in switches:
            query = self.forge_query(pk, switch.pk, period)
            data = self.forge_data(query, unit)
            datas_non_aggregated.extend(data)

        if pk.count() == 1:
            return datas_non_aggregated

        datas_non_aggregated.sort(key=lambda stat: stat.get("time"))
        datas_aggregated = []
        time_cursor = self.time_first_value
        value = 0
        for data in datas_non_aggregated:
            if ((data["time"] - time_cursor) >= timedelta(seconds=0)) &\
                    ((data["time"] - time_cursor) <= timedelta(seconds=self.probe_time_interval)):
                value += data["value"]
            else:
                datas_aggregated.append({
                    "value": value,
                    "time": time_cursor
                })
                time_cursor = data["time"]
                value = data["value"]
        return datas_aggregated

    def get_flux_id(self, source="0", destination="0", flux_type="IPv4"):

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

    def forge_query(self, pk, dpid, period='day'):
        liste_pk = []
        for primary in pk:
            liste_pk.append(primary.get('idflux'))
        query = Stats.objects.filter(idflux__in=liste_pk).filter(idswitch_id=dpid)

        query = query.filter(time__gte=self.get_start_time(period))

        query = query.order_by("time")

        query = query.values("time").annotate(bytes=Sum('bytes'), packets=Sum('packets'))

        return query

    def forge_data(self, stats, unit='bytes'):
        data_list = []
        for index, stat in list(enumerate(stats)):
            try:
                next = stats[index + 1]
            except IndexError:
                # No more values
                break

            value = ((next.get(unit) - stat.get(unit)) / self.diff_seconds(next.get('time'), stat.get('time')))
            data = {'time': next.get('time'),
                    'value': int(value)}
            data_list.append(data)

            if next["time"] < self.time_first_value:
                self.time_first_value = next["time"]

        return data_list

    def diff_seconds(self, datetime1, datetime2):
        if datetime2 >= datetime1:
            time_diff = datetime2 - datetime1
        else:
            time_diff = datetime1 - datetime2
        return time_diff.total_seconds()

    def get_start_time(self, period="day"):
        if period == "hour":
            return self.now - timedelta(hours=1)
        elif period == "day":
           return self.now - timedelta(days=1)
        elif period == "month":
            return self.now - timedelta(days=31)
        elif period == "year":
            return self.now - timedelta(days=366)
