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



import re

from django.utils.translation import ugettext_lazy as _
from django.forms import fields
from django.db import models
from django.db.models.fields import BigIntegerField

MAC_RE = r'^([0-9a-fA-F]{2}([:]?|$)){6}$'
mac_re = re.compile(MAC_RE)


# snippet from : https://djangosnippets.org/snippets/1337/
class MACAddressFormField(fields.RegexField):
    """
    Class for customise the regexField class, with special error message for our use case.
    """
    default_error_messages = {
        'invalid': _(u'Entrez une adresse MAC valide. (caractères autorisés : 0-9 a-f A-F : )'),
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(mac_re, *args, **kwargs)


class MACAddressField(models.Field):
    """
    This class represents a Mac address field for the model representation.
    It limits the maximum number for CharField, plus a regular expression verification when modifying data.
    """
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)


# Snippet found in : https://news.numlock.ch/it/django-custom-model-field-for-an-unsigned-bigint-data-type
class PositiveBigIntegerField(BigIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "BigIntegerField"

    def db_type(self, connection):
        # This is how MySQL defines 64 bit unsigned integer data types
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "bigint UNSIGNED"
        elif connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return "NUMERIC(20,0)"
        else:
            return "NUMERIC(20,0)"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super(PositiveBigIntegerField, self).formfield(**defaults)