# -*- coding: utf8 -*-
__author__ = 'remy'
from django import forms

from database.models import Hote


class MemberChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):

        super(MemberChoiceField, self).__init__(choices, required, widget, label, initial, help_text, *args, **kwargs)
        query = Hote.objects.filter(valid=True)
        self.choices.append(("0", "ALL"))

        for member in query:
            self.choices.append((str(member.pk), member.nomhote))

class UnitForm (forms.Form):
    unit = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('packets', 'Packets',),
                                      ('bytes', 'Bytes',),))

    def get_unit(self):
        return self.cleaned_data["unit"]

class PeriodFrom(forms.Form):

    period = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                               choices=(('hour', 'hour',),
                                      ('day', 'day',),
                                      ('month', 'month',),
                                      ('year', 'year',),))

    def get_period(self):
        return self.cleaned_data["period"]

class TypeForm(forms.Form):
    type = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('IPv6', 'IPv6',),
                                    ('IPv4', 'IPv4',),
                                    ('ARP', 'ARP',),
                                    ('ICMPv6', 'ICMPv6',),))

    def get_type(self):
        return self.cleaned_data["type"]
class SourceForm(forms.Form):
    source = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    def get_source(self):
        return self.cleaned_data["source"]
class DestinationForm(forms.Form):
    destination = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    def get_destination(self):
        return self.cleaned_data["destination"]

class FluxSelectionForm(SourceForm, DestinationForm, TypeForm, UnitForm, PeriodFrom):
    pass

class RestrictedFluxSelectionForm(PeriodFrom, TypeForm, UnitForm):
    pass






