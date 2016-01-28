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
from django import forms

from Database.models import Hote
from django.db.utils import ProgrammingError

class MemberChoiceField(forms.ChoiceField):
    """
    Choicefield modified to get the list of all the valid routers present in the topology,
    and a choice for select all of them.
    """
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):

        super(MemberChoiceField, self).__init__(choices, required, widget, label, initial, help_text, *args, **kwargs)
        # Check if table exists
        try:
            Hote.objects.all().get()
        except ProgrammingError:
            # TODO find a better solution to check if table exists
            self.choices.append(("", "None"))
            return None
        except Hote.DoesNotExist:
            LOG.warning("No entries in host model. Statistics app will not perform correctly.")

        query = Hote.objects.filter(valid=True)
        self.choices.append(("0", "ALL"))

        for member in query:
            self.choices.append((str(member.pk), member.nomhote))


class UnitForm (forms.Form):
    """
    Choice form for selecting unit output.
    """
    unit = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('packets', 'Packets',),
                                      ('bytes', 'Bytes',),))

    def get_unit(self):
        return self.cleaned_data["unit"]


class PeriodFrom(forms.Form):
    """
    Choice form for select the period.
    """
    period = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                               choices=(('day', 'day',),
                                      ('week', 'week',),
                                      ('month', 'month',),
                                      ('year', 'year',),))

    def get_period(self):
        return self.cleaned_data["period"]


class TypeForm(forms.Form):
    """
    Choice form for select the flow type.
    """
    type = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('IPv6', 'IPv6',),
                                    ('IPv4', 'IPv4',),
                                    ('ARP', 'ARP',),
                                    ('ICMPv6', 'ICMPv6',),))

    def get_type(self):
        return self.cleaned_data["type"]


class SourceForm(forms.Form):
    """
    Choicefield form reprensenting the flow source.
    """
    source = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    def get_source(self):
        return self.cleaned_data["source"]


class DestinationForm(forms.Form):
    """
    Choicefield form reprensenting the flow destination.
    """
    destination = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    def get_destination(self):
        return self.cleaned_data["destination"]


class FluxSelectionForm(DestinationForm, SourceForm, TypeForm, PeriodFrom):
    """
    Form for authenticated users
    """
    pass


class RestrictedFluxSelectionForm(PeriodFrom, TypeForm):
    """
    Form for non-authenticated users
    """
    pass
