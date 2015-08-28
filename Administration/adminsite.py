# -*- coding: utf8 -*-
__author__ = 'remy'
from django.contrib.admin import AdminSite


class TouSIXAdmin(AdminSite):
    """
    Special admin site, created for display widgets in the main panel.
    """
    site_header = "TouIX - Administration de TouSIX"
    site_title = "TouIX"
    index_template = "index_touSIX.html"


admin_tousix = TouSIXAdmin(name='Administration')
