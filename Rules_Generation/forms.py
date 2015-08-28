# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms

from Database.models import Switch


class SwitchMultipleSelectField(forms.ModelMultipleChoiceField):
    """
    This class rewrites the original behavior of ModelMultipleChoiceField for showing the switch name as label.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.nomswitch

class SwitchChoiceForm(forms.Form):
    """
    A form that shows all the avaliables switches for a imple selection (not necessary with the admin integration)
    """
    switches = SwitchMultipleSelectField(widget=forms.CheckboxSelectMultiple(),
                                         queryset=Switch.objects.all())

    def get_selected(self):
        return self.cleaned_data["switches"]
