from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import IndexView, HumansView, BlogView
from .feeds import LatestEntriesFeed
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.shortcuts import redirect


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^humans.txt/$', HumansView.as_view(), name='humans'),
    url(r'^v1/', include('allmychanges.urls_api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/$', BlogView.as_view(), name='blog'),
    url(r'^blog/feed/$', LatestEntriesFeed(), name='blog-feed'),
    url(r'^favicon.ico/$', lambda x: redirect('/static/favicon.ico')),
    url(r'^django-rq/', include('django_rq.urls')),
)

urlpatterns += staticfiles_urlpatterns()

