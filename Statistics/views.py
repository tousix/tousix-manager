from django.views.generic.edit import FormView
from Statistics.forge import forgeData
from Statistics.forms import FluxSelectionForm
from Statistics.JSONResponseMixin import JSONResponseMixin

# Create your views here.


class StatsMembersList(FormView, JSONResponseMixin):
    template_name = 'stats_list.html'
    form_class = FluxSelectionForm

    def form_valid(self, form):

        data = forgeData.get_data(form.get_source(), form.get_destination(), form.get_type(), form.get_period(), form.get_unit())

        return JSONResponseMixin.render_to_response(self, data)
