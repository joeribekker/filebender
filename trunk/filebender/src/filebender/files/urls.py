from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list/$', 'files.views.list'),
    (r'^download/(?P<file_id>\d+)/$', 'files.views.download'),
    (r'^upload/$', 'files.views.upload'),
)
