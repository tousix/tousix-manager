#    Copyright 2015 Rémy Lapeyrade <rlapeyra at laas dot fr>
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
from django.utils.timezone import timedelta, now
from influxdb import InfluxDBClient
from django.conf import settings


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
            return "1w"
        elif period == "day":
            return "1d"
        elif period == "month":
            return "31d"
        elif period == "year":
            return "366d"

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
        query = self.forge_query(source, destination, flow_type, self.now, period)

        settings_influx = settings.INFLUXDB_CONFIG
        influx_client = InfluxDBClient(host=settings_influx.get("host", "localhost"),
                                       port=settings_influx.get('port',8086),
                                       username=settings_influx.get("user",'root'),
                                       password=settings_influx.get("password",'root'),
                                       database=settings_influx.get("database","default"),
                                       ssl=settings_influx.get("use_ssl",False),
                                       verify_ssl=settings_influx.get('safe_ssl', True))

        data = influx_client.query(query=query)

        return list(data.get_points())

    def forge_query(self, source='0', destination= '0', flow_type='IPv4', time=now().isoformat(), period='day', unit='bytes'):
        """
        Create influxDB query and retrieve values.
        :param source:
        :param destination:
        :param flow_type:
        :param time:
        :param period:
        :param unit:
        :return:
        """
        measurement = "value"
        query = "select non_negative_derivative(sum({0}),{1}) as value" \
                " from {2} where " \
                "{3} " \
                "group by time({4}) fill({5})"
        rate = "1s"
        time_start = self.get_start_time(period)

        # forge field
        if unit is "bytes":
            field = "byte_count"
        elif unit is "packets":
            field = "packet_count"

        # forge conditions
        conditions = "type='{0}'".format(flow_type)
        conditions += " and time > {0}".format("now()")
        conditions += " - {0}".format(time_start)

        if source is not "0":
            conditions += " and source='{0}'".format(source)
        if destination is not "0":
            conditions += " and destination='{0}'".format(destination)
        group_by = self.set_time_interval(period)
        fill = "null"

        # format query strign
        query = query.format(measurement, rate, field, conditions, group_by, fill)

        # forge group by (time interval and tolerance)
        return query

    def set_time_interval(self, period='day'):
        """
        Set time interval to create downsampling effect on values.
        :param period:
        :return:
        """
        if period == 'day':
            return "5m,4m"
        elif period == 'week':
            return "40m, 4m"
        elif period == "month":
            return "1h,4m"
        elif period == "year":
            return "18h,4m"
        else:
            return "5m,4m"

