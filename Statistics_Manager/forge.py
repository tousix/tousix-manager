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
from django.db.models import Sum
from django.utils.timezone import timedelta, now

from Database.models import Flux, Stats, Switch


class forgeData(object):
    """
    Class for handling statistics requests.
    The output model for dataset is the following (Python objects)::

        [{'time': datetime,
          'value': integer},
          {'time': datetime,
          'value': integer},
          ...]
    The input in the dict is not guaranteed to be chronological.
    """
    # delta time time between first and last stat value of the same request
    time_interval = 5
    # initial time value
    time_first_value = now()

    def get_data(self, source, destination, flow_type, period, unit):
        """
        Main method for construct the dataset based on user input.
        If multiple flows are present in the results, it will be aggregated based on time differential between values.
        :param source: source host ID
        :param destination: destination host ID
        :param flow_type: Flow type
        :param period: Time period asked by the user
        :param unit: Output unit (packets or bytes)
        :return:
        """
        self.now = now()
        pk = self.get_flow_id(source, destination, flow_type)
        datas_non_aggregated = []
        query = self.forge_query(pk, period)
        data = self.forge_data(query, unit)
        datas_non_aggregated.extend(data)
        #
        # # only one flow to extract => no need for supplementary aggregations
        # if pk.count() == 1:
        #     return datas_non_aggregated
        #
        # # sort all values in chronological period
        # datas_non_aggregated.sort(key=lambda stat: stat.get("time"))
        #
        # datas_aggregated = []
        #
        # # set cursor on the earliest stat (done in forge_data)
        # time_cursor = self.time_first_value
        # value = 0
        # for data in datas_non_aggregated:
        #     # if the data is in the time interval, add the value
        #     if ((data["time"] - time_cursor) >= timedelta(seconds=0)) &\
        #             ((data["time"] - time_cursor) <= timedelta(seconds=self.time_interval)):
        #         value += data["value"]
        #     # else, register the aggregated data and move the cursor
        #     else:
        #         datas_aggregated.append({
        #             "value": value,
        #             "time": time_cursor
        #         })
        #         time_cursor = data["time"]
        #         value = data["value"]
        return datas_non_aggregated

    def get_flow_id(self, source="0", destination="0", flow_type="IPv4"):
        """
        Retrieve all the flow based on user input.
        :param source: source host ID
        :param destination: destination host ID
        :param flow_type: Flow type
        :return:
        """
        query = Flux.objects.all()
        # flow types with no sources have null value on source column
        if flow_type == "ICMPv6" or flow_type == "ARP":
            query = query.filter(hote_src_id__isnull=True)

        elif source is not "0":
            query = query.filter(hote_src_id=source)

        if destination is not "0":
            query = query.filter(hote_dst_id=destination)

        query = query.filter(type=flow_type)
        liste_pk = query.values('idflux')
        return liste_pk

    def forge_query(self, pk, period='day'):
        """
        Create Django query and retrieve values.
        :param pk:
        :param dpid:
        :param period:
        :return:
        """
        liste_pk = []
        for primary in pk:
            liste_pk.append(primary.get('idflux'))
        # filter stats by flow and switch origin
        query = Stats.objects.filter(idflux__in=liste_pk)

        query = query.filter(time__gte=self.get_start_time(period))

        # needed for conversion into average value
        query = query.order_by("time")

        # sum on all the flow with the same time
        query = query.values("time").annotate(bytes=Sum('bytes')
                                              #,packets=Sum('packets')
                                              )

        return query

    def forge_data(self, stats, unit='bytes'):
        """
        Calculate bandwidth speed.
        :param stats:
        :param unit:
        :return:
        """
        data_list = []
        # create a special list for retrieve the next value
        for index, stat in list(enumerate(stats)):
            try:
                next = stats[index + 1]
            except IndexError:
                # No more values in the list
                break

            # average value in an time interval (second based)
            value = ((next.get('bytes') - stat.get('bytes')) / self.diff_seconds(next.get('time'), stat.get('time')))
            if value < 0:
                value = 0
            if unit == 'bits':
                value *= 8
            data = {'time': next.get('time'),
                    'value': int(value)}
            data_list.append(data)

            # update the earliest value in the data
            if next["time"] < self.time_first_value:
                self.time_first_value = next["time"]

        return data_list

    def diff_seconds(self, datetime1, datetime2):
        """
        Get the difference between two datetimes in seconds.
        :param datetime1:
        :param datetime2:
        :return:
        """
        if datetime2 >= datetime1:
            time_diff = datetime2 - datetime1
        else:
            time_diff = datetime1 - datetime2
        return time_diff.total_seconds()

    def get_start_time(self, period="day"):
        """
        Returns a datetime for query calculations.
        :param period:
        :return:
        """
        if period == "week":
            return self.now - timedelta(days=8)
        elif period == "day":
            return self.now - timedelta(days=1)
        elif period == "month":
            return self.now - timedelta(days=31)
        elif period == "year":
            return self.now - timedelta(days=366)
