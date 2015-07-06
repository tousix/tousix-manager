# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms

from database.models import Switch


class SwitchMultipleSelectField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.nomswitch

class SwitchChoiceForm(forms.Form):
    switches = SwitchMultipleSelectField(widget=forms.CheckboxSelectMultiple(),
                                         queryset=Switch.objects.all())

    def get_selected(self):
        return self.cleaned_data["switches"]
