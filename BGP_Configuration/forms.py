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
