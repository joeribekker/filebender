from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^list/$', 'files.views.list'),
    (r'^download/(?P<id>\d+)/(?P<secret>\w{50})/$', 'files.views.download'),
    (r'^delete/(?P<id>\d+)/$', 'files.views.delete'),
    (r'^upload/$', 'files.views.upload'),
    (r'^$', 'files.views.list'),
)
# TODO: replace 50 with settings.FILE_SECRET_LENGTH