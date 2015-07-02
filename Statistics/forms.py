# -*- coding: utf8 -*-
__author__ = 'remy'
from django import forms

from database.models import Hote


class JavasciptWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super(JavasciptWidget, self).__init__(attrs, choices)

class MemberChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):

        super(MemberChoiceField, self).__init__(choices, required, widget, label, initial, help_text, *args, **kwargs)
        query = Hote.objects.all()
        self.choices.append(("0", "ALL"))

        for member in query:
            self.choices.append((str(member.pk), member.nomhote))

class FluxSelectionForm(forms.Form):
    source = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    destination = MemberChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}))

    type = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('IPv6', 'IPv6',),
                                    ('IPv4', 'IPv4',),
                                    ('ARP', 'ARP',),
                                    ('ICMPv6', 'ICMPv6',),))

    period = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                               choices=(('hour', 'hour',),
                                      ('day', 'day',),
                                      ('month', 'month',),
                                      ('year', 'year',),))

    unit = forms.ChoiceField(widget=forms.Select(attrs={"onchange": "FormChanged(this.form);"}),
                             choices=(('packets', 'Packets',),
                                    ('bytes', 'Bytes',),))

    def get_source(self):
        return self.cleaned_data["source"]

    def get_destination(self):
        return self.cleaned_data["destination"]

    def get_type(self):
        return self.cleaned_data["type"]

    def get_period(self):
        return self.cleaned_data["period"]

    def get_unit(self):
        return self.cleaned_data["unit"]


