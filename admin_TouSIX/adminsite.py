# -*- coding: utf8 -*-
__author__ = 'remy'
from django.contrib.admin import AdminSite


class TouSIXAdmin(AdminSite):
    site_header = "TouIX - Administration de TouSIX"
    site_title = "TouIX"
    index_template = "index_touSIX.html"


admin_tousix = TouSIXAdmin(name='admin_TouSIX')
