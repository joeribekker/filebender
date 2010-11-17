from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list/$', 'files.views.list'),
    (r'^download/(?P<id>\d+)/$', 'files.views.download'),
    (r'^delete/(?P<id>\d+)/$', 'files.views.delete'),
    (r'^upload/$', 'files.views.upload'),
    (r'^$', 'files.views.list'),
)
