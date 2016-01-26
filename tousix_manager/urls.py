"""web_TouSIX URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin

from tousix_manager.Frontpages import WelcomeView
from tousix_manager.Log_Controller.views import AsyncEventView
from tousix_manager.Log_Statistics.views import RecieveStatsForm
from tousix_manager.Member_Manager import urls as members_urls
from tousix_manager.Rules_Deployment import urls as rules_deployment_urls
from tousix_manager.Statistics_Manager import urls as statistics_urls

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin_tousix/', include(admin_tousix.urls)),
    url(r'^event/', AsyncEventView.as_view(), name='Async event log'),
    url(r'^member', include(members_urls)),
    url(r'^plot', RecieveStatsForm.as_view(), name='Recieve stats'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^deployment', include(rules_deployment_urls)),
    url(r'^django-sb-admin/', include('django_sb_admin.urls')),
    url(r'^stats', include(statistics_urls)),
    url(r'^', WelcomeView.as_view(), name='welcome page'),

]
