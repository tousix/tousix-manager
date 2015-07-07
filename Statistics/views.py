from django.views.generic.edit import FormView
from Statistics.forge import forgeData
from Statistics.forms import FluxSelectionForm, RestrictedFluxSelectionForm
from Statistics.JSONResponseMixin import JSONResponseMixin
from Authentication.LoginMixin import LoginRequiredMixin
# Create your views here.


class StatsMembersList(LoginRequiredMixin, FormView, JSONResponseMixin):
    template_name = 'stats_list.html'
    form_class = FluxSelectionForm

    def form_valid(self, form):
        forge = forgeData()
        data = forge.get_data(form.get_source(), form.get_destination(), form.get_type(), form.get_period(), form.get_unit())

        return JSONResponseMixin.render_to_response(self, data)

class RestrictedStats(FormView, JSONResponseMixin):
    template_name = 'restricted_chart.html'
    form_class = RestrictedFluxSelectionForm

    def form_valid(self, form):
        forge = forgeData()
        data = forge.get_data('0', '0', form.get_type(), form.get_period(), form.get_unit())

        return JSONResponseMixin.render_to_response(self, data)
