from django.views.generic.edit import FormView
from Statistics.forge import forgeData
from database.models import Membre
from django.shortcuts import render, redirect
from Statistics.forms import FluxSelectionForm, RestrictedFluxSelectionForm
from Statistics.JSONResponseMixin import JSONResponseMixin
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
