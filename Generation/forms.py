# -*- coding: utf8 -*-
__author__ = 'remy'

from django import forms

from database.models import Membre


class MembersMultipleSelectField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.nommembre


class MembersChoiceForm(forms.Form):
    members = MembersMultipleSelectField(widget=forms.CheckboxSelectMultiple(),
                                         queryset=Membre.objects.exclude(nommembre="TouIX"))

    def get_selected(self):
        return self.cleaned_data["members"]
