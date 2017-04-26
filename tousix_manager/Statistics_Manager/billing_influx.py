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

import math
from django.utils.timezone import timedelta, now
from influxdb import InfluxDBClient
from django.conf import settings


class BillingView(object):
    """
    Generic class to retrieve the value of bandwidth necessary for billing.
    This module stay apart from the Django app, due to heavy resources consumption.
    But it can be adapted to be executed as a background task (Celery job for example).
    """
    def initialize_time(self):
        self.date = now().replace(microsecond=0)
        self.last_year = self.date - timedelta(days=365)

    def config_influx(self):
        settings_influx = settings.INFLUXDB_CONFIG
        influx_client = InfluxDBClient(host=settings_influx.get("host", "localhost"),
                                       port=settings_influx.get('port',8086),
                                       username=settings_influx.get("user",'root'),
                                       password=settings_influx.get("password",'root'),
                                       database=settings_influx.get("database","default"),
                                       ssl=settings_influx.get("use_ssl",False),
                                       verify_ssl=settings_influx.get('safe_ssl', True))
        return influx_client

    def get_result(self, influx_client, hostid):

        query = "select non_negative_derivative(sum(value),1s) as value" \
                " from {0} where {1}" \
                " group by time({2}) fill({3})"
        field = "byte_count"
        condition = "(source='{0}' or destination='{0}') and {1}"
        time = "time >= '" + self.last_year.isoformat(' ') + "' and time < '" + self.date.isoformat(' ') + "'"
        condition = condition.format(hostid, time)
        fill = "null"
        group_by = "5m,4m"
        query = query.format(field, condition, group_by, fill)
        data = influx_client.query(query=query)
        points = list(data.get_points())

        return [x.get('value') for x in points]

    def show_result(self, host_id):
        result = self.get_result(self.influx_client, host_id)
        return int(percentile(result, 0.95))

    def __init__(self):
        self.influx_client = self.config_influx()
        self.initialize_time()


def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1
