# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms

from Database.models import Membre


class MembersMultipleSelectField(forms.ModelMultipleChoiceField):
    """
    ModelMultipleChoiceField with modified label.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.nommembre


class MembersChoiceForm(forms.Form):
    """
    Form for members selection, excluding the TouIX member
    """
    members = MembersMultipleSelectField(widget=forms.CheckboxSelectMultiple(),
                                         queryset=Membre.objects.exclude(nommembre="TouIX"))

    def get_selected(self):
        return self.cleaned_data["members"]
