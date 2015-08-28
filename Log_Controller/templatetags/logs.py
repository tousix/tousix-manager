# -*- coding: utf8 -*-
__author__ = 'remy'

from django import template
from Database.models import LogSwitch
register = template.Library()

@register.assignment_tag(name="pull_logs")
def pull_logs():
    return LogSwitch.objects.all()
