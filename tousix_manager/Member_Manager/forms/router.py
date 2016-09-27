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

from tousix_manager.Database.models import Hote


class RouterForm(forms.ModelForm):
    """
    ModelForm for router model.
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):

        super(RouterForm, self).__init__(data, files, auto_id, prefix,
                                         initial, error_class, label_suffix,
                                         empty_permitted, instance)

        self.fields['ipv4hote'].widget.attrs['readonly'] = True
        self.fields['ipv6hote'].widget.attrs['readonly'] = True

    def clean_ipv4hote(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.ipv4hote
        else:
            return self.cleaned_data['ipv4hote']

    def clean_ipv6hote(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.ipv6hote
        else:
            return self.cleaned_data['ipv6hote']

    class Meta:
        model = Hote
        fields = ['nomhote', 'ipv4hote', 'ipv6hote', 'machote']

class NewRouterForm(forms.ModelForm):

    class Meta:
        model = Hote
        fields = ['nomhote', 'machote']
        exclude = ['ipv4hote', 'ipv6hote']