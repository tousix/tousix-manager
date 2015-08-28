# -*- coding: utf8 -*-
__author__ = 'remy'
"""Member_Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from Member_Manager.views import CreateMemberView, UpdateMemberView, NOCUpdateView, BillingUpdateView, TechnicalUpdateView, RouterUpdateView, PasswordChangeView

urlpatterns = [

    url(r'^/update/technical', TechnicalUpdateView.as_view(), name='update technical'),
    url(r'^/update/noc', NOCUpdateView.as_view(), name='update noc'),
    url(r'^/update/billing', BillingUpdateView.as_view(), name='update billing'),
    url(r'^/update/router', RouterUpdateView.as_view(), name='update router'),
    url(r'^/update/password', PasswordChangeView.as_view(), name='update password'),
    url(r'^/update', UpdateMemberView.as_view(), name='update member'),
    url(r'^/create', CreateMemberView.as_view(), name='Create member'),
]
