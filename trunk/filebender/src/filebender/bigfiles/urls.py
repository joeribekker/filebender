from django.conf.urls.defaults import patterns
from django.conf import settings

urlpatterns = patterns('',
    (r'^list/$', 'bigfiles.views.list'),
    (r'^download/(?P<id>\d+)/(?P<secret>\w{%i})/$' % settings.FILE_SECRET_LENGTH,
        'bigfiles.views.download'),
    (r'^delete/(?P<id>\d+)/$', 'bigfiles.views.delete'),
    (r'^upload/$', 'bigfiles.views.upload'),
    (r'^$', 'bigfiles.views.list'),
)
# TODO: replace 50 with settings.FILE_SECRET_LENGTH