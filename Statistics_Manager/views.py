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

from django.views.generic.edit import FormView
from Statistics_Manager.forge import forgeData
from Database.models import Membre
from django.shortcuts import render, redirect
from Statistics_Manager.forms import FluxSelectionForm, RestrictedFluxSelectionForm
from Statistics_Manager.JSONResponseMixin import JSONResponseMixin
from Authentication.LoginMixin import LoginRequiredMixin
from django.core.urlresolvers import reverse
# Create your views here.


class StatsMembersList(LoginRequiredMixin, FormView, JSONResponseMixin):
    """
    View for display network statistics (authenticated users only)
    """
    template_name = 'stats_list.html'
    form_class = FluxSelectionForm

    def get(self, request, *args, **kwargs):

        membre = Membre.objects.filter(user=self.request.user)
        if membre.count() > 0:
            if membre.first().approved is True:
                return super(StatsMembersList, self).get(request, *args, **kwargs)
            else:
                return render(request, self.template_name, context={"not_member": True,
                                                                    "member": membre.first()})
        context = {"not_member": True}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        membre = Membre.objects.filter(user=self.request.user)
        if membre.count() > 0:
            if membre.first().approved is True:
                return super(StatsMembersList, self).post(request, *args, **kwargs)
        return JSONResponseMixin.render_to_response(self, [])

    def form_valid(self, form):
        forge = forgeData()
        data = forge.get_data(form.get_source(), form.get_destination(), form.get_type(), form.get_period(), form.get_unit())

        return JSONResponseMixin.render_to_response(self, data)


class RestrictedStats(FormView, JSONResponseMixin):
    """
    View for display network statistics (non-authenticated users only)
    This view is the same as StatsMembersList, but with restricted options.
    """
    template_name = 'restricted_chart.html'
    form_class = RestrictedFluxSelectionForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return super(RestrictedStats, self).get(request, *args, **kwargs)
        return redirect(reverse("charts"))

    def form_valid(self, form):
        forge = forgeData()
        data = forge.get_data('0', '0', form.get_type(), form.get_period(), form.get_unit())

        return JSONResponseMixin.render_to_response(self, data)
