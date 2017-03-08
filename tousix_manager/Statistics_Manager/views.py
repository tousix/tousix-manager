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
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.core.cache import caches
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from tousix_manager.Authentication.LoginMixin import LoginRequiredMixin
from tousix_manager.Database.models import UserMembre, Hote
from tousix_manager.Statistics_Manager.JSONResponseMixin import JSONResponseMixin
from tousix_manager.Statistics_Manager.forge import forgeData
from tousix_manager.Statistics_Manager.forge_influx import forgeData as forgeDataInflux
from tousix_manager.Statistics_Manager.forms import FluxSelectionForm, RestrictedFluxSelectionForm
from django.conf import  settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import JsonResponse
# Create your views here.


class StatsMembersList(LoginRequiredMixin, FormView, JSONResponseMixin):
    """
    View for display network statistics (authenticated users only)
    """
    template_name = 'stats_list.html'
    form_class = FluxSelectionForm

    def get(self, request, *args, **kwargs):

        if UserMembre.objects.filter(user=self.request.user).count() > 0:
            membre = UserMembre.objects.filter(user=self.request.user).first().membre
            if membre is not None:
                if membre.approved is True:
                    return super(StatsMembersList, self).get(request, *args, **kwargs)
        return redirect(reverse("restricted stats"))

    def post(self, request, *args, **kwargs):
        membre = UserMembre.objects.filter(user=self.request.user).first().membre
        if membre is not None:
            if membre.approved is True:
                return super(StatsMembersList, self).post(request, *args, **kwargs)
        return JSONResponseMixin.render_to_response(self, [])

    def form_valid(self, form):
        cache_statistics = caches['statistics']
        composed_request = str(form.get_source()) + str(form.get_destination()) + form.get_type() + form.get_period() + 'bytes'
        cache_value = cache_statistics.get(composed_request, None)
        if not self.request.user.is_staff:
            id_membre = UserMembre.objects.filter(user=self.request.user).first().membre.idmembre
            if self.verify_data_access(id_membre, form) is "Forbidden":
                raise PermissionDenied
            if form.get_destination() == form.get_source():
                raise PermissionDenied
        if cache_value is None:
            if settings.INFLUXDB_ENABLE:
                forge = forgeDataInflux()
            else:
                forge = forgeData()
            data = forge.get_data(source=form.get_source(),
                                  destination=form.get_destination(),
                                  flow_type=form.get_type(),
                                  period=form.get_period(),
                                  unit='bytes')
            if data is None:
                return JsonResponse({}, status=403)
            cache_statistics.set(composed_request, data)
            return JSONResponseMixin.render_to_response(self, data)
        else:
            return JSONResponseMixin.render_to_response(self, cache_value)

    def verify_data_access(self, id, form):
        if not (form.get_source() is '0' and form.get_destination() is '0'):
            try:
                Hote.objects.filter(idhote__in=[form.get_source(),form.get_destination()]).get(idmembre=id)
            except Hote.DoesNotExist:
                return "Forbidden"
        return None

class RestrictedStats(FormView, JSONResponseMixin):
    """
    View for display network statistics (non-authenticated users only)
    This view is the same as StatsMembersList, but with restricted options.
    """
    template_name = 'restricted_chart.html'
    form_class = RestrictedFluxSelectionForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or UserMembre.objects.filter(user=self.request.user).count() == 0:
            return super(RestrictedStats, self).get(request, *args, **kwargs)
        return redirect(reverse("charts"))

    def form_valid(self, form):
        cache_statistics = caches['statistics']
        composed_request = '0' + '0' + form.get_type() + form.get_period() + 'bytes'
        cache_value = cache_statistics.get(composed_request, None)
        if cache_value is None:
            if settings.INFLUXDB_ENABLE:
                forge = forgeDataInflux()
            else:
                forge = forgeData()
            data = forge.get_data('0', '0', form.get_type(), form.get_period(), 'bytes')
            cache_statistics.set(composed_request, data)
            return JSONResponseMixin.render_to_response(self, data)
        else:
            return JSONResponseMixin.render_to_response(self, cache_value)
