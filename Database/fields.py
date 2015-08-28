# -*- coding: utf8 -*-
__author__ = 'remy'



import re

from django.utils.translation import ugettext_lazy as _
from django.forms import fields
from django.db import models
from django.db.models.fields import PositiveIntegerField

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
class PositiveBigIntegerField(PositiveIntegerField):
    """Represents MySQL's unsigned BIGINT data type (works with MySQL only!)"""
    empty_strings_allowed = False

    def get_internal_type(self):
        return "PositiveBigIntegerField"

    def db_type(self, connection):
        # This is how MySQL defines 64 bit unsigned integer data types
        return "bigint UNSIGNED"
