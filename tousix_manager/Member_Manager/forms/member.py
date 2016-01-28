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

from tousix_manager.Database.models import Membre, ConnectionType


class ConnexionChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display connection type information.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.connection_type


class MemberForm(forms.ModelForm):
    """
    ModelForm with custom field for display connectiontype value.
    """
    connexion_type = ConnexionChoiceField(queryset=ConnectionType.objects.all(), empty_label=None)

    class Meta:
        model = Membre
        fields = ['nommembre', 'url', 'asnumber', 'connexion_type', 'fqdn_host']
