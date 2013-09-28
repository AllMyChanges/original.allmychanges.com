from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import IndexView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^v1/', include('allmychanges.urls_api')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

