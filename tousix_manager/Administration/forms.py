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
from django.forms.utils import ErrorList
from tousix_manager.Database.models import Hote, Port, Switch, Pop, Membre, ConnectionType, UserMembre, Switchlink


class PortChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display complete port information.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.string_description()


class HoteForm(forms.ModelForm):
    """
    ModelForm with custom router display.
    This form handles the link between :model:`Database.Port` and :model:`Database.Hote`.
    Depending of the context (relationship non-established, initial value), it will
    create a custom list with complete description all the ports avaliable.
    """
    idport = PortChoiceField(queryset=Port.objects
                             .filter(enabled=True), empty_label=None)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None, use_required_attribute=None):
        super(HoteForm, self).__init__(data, files, auto_id, prefix,
                                       initial, error_class, label_suffix,
                                       empty_permitted, instance, use_required_attribute)
        if self.instance.idhote is not None:
            # Set idport editing value for instance
            self.fields["idport"].queryset = Port.objects.filter(enabled=True)
            if self.instance.idport is not None:
                self.fields["idport"].initial = {self.instance.idport_id: self.instance.idport.string_description}

    class Meta:
        model = Hote
        exclude = ["idmembre"]


class PopChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display POP name instead of complete object.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.nompop


class SwitchForm(forms.ModelForm):
    """
    ModelForm for modify :model:`Database.Switch` with custom fields.
    """
    idpop = PopChoiceField(queryset=Pop.objects.all(), empty_label=None)

    class Meta:
        model = Switch
        fields = ['nomswitch', 'dpid_switch', 'ipswitch', 'idpop', 'faucet_class']


class SwitchChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display Switch name instead of complete object.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.nomswitch


class PortForm(forms.ModelForm):
    """
    ModelForm for modify :model:`Database.Port` with custom fields.
    """
    idswitch = SwitchChoiceField(queryset=Switch.objects.all(), empty_label=None)

    class Meta:
        model = Port
        fields = ['idswitch', 'numport', 'typeport', 'enabled', 'backbone']


class ConnexionChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display Connection type name instead of complete object.
    """
    def label_from_instance(self, obj):
        return "%s" % obj.connection_type


class MembreForm(forms.ModelForm):
    """
    ModelForm for modify :model:`Database.Membre` with custom fields.
    """
    idpop = PopChoiceField(queryset=Pop.objects.all())
    connexion_type = ConnexionChoiceField(queryset=ConnectionType.objects.all())

    class Meta:
        model = Membre
        fields = ["nommembre", "asnumber", "connexion_type", "fqdn_host", "idpop", "approved", "login_external"]


class MemberChoiceField(forms.ModelChoiceField):
    """
    ModelChoiceField modification for display member name instead of complete object.
    """

    def label_from_instance(self, obj):
        return "%s" % obj.nommembre


class UserMembreForm(forms.ModelForm):
    membre = MemberChoiceField(queryset=Membre.objects.all(), empty_label=None)

    class Meta:
        model = UserMembre
        fields = ['user', 'membre']


class SwitchlinkForm(forms.ModelForm):

    def label_from_instance(self, obj):
        return "%s" % obj.string_description

    class Meta:
        model = Switchlink
        fields = ['idport1', 'idport2']