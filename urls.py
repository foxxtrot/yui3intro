from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^checkin/$', 'yui3intro.checkin.views.index'),
    (r'^checkin/checkin/(?P<registration_id>\d+)$', 'yui3intro.checkin.views.checkin'),
    (r'^checkin/filter/(?P<filter_text>[\w%\d]+)$', 'yui3intro.checkin.views.filter'),
    (r'^checkin/filter/(?P<filter_text>[\w\d%]+)/page/(?P<page_number>\d+)$', 'yui3intro.checkin.views.filter'),
    (r'^checkin/filter/$', 'yui3intro.checkin.views.filter'),
    (r'^checkin/page/(?P<page_number>\d+)$', 'yui3intro.checkin.views.index'),
    (r'^checkin/stats$', 'yui3intro.checkin.views.stats'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'static', 'show_indexes': True }),
    (r'^admin/', include(admin.site.urls)),
)
