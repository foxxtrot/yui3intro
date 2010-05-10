from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^checkin/$', 'pcc2010.checkin.views.index'),
    (r'^checkin/checkin/(?P<registration_id>\d+)$', 'pcc2010.checkin.views.checkin'),
    (r'^checkin/filter/(?P<filter_text>[\w%\d]+)$', 'pcc2010.checkin.views.filter'),
    (r'^checkin/filter/(?P<filter_text>[\w\d%]+)/page/(?P<page_number>\d+)$', 'pcc2010.checkin.views.filter'),
    (r'^checkin/filter/$', 'pcc2010.checkin.views.filter'),
    (r'^checkin/page/(?P<page_number>\d+)$', 'pcc2010.checkin.views.index'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': 'static', 'show_indexes': True }),
    (r'^admin/', include(admin.site.urls)),
)
