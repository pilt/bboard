from django.conf import settings
from django.conf.urls.defaults import *
from django.template import add_to_builtins

from django.contrib import admin
admin.autodiscover()

import nexus
nexus.autodiscover()

add_to_builtins('django.templatetags.i18n')

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^sentry/', include('sentry.urls')),
    ('^nexus/', include(nexus.site.urls)),
    #('^', include('haystack.urls')),
    (r'^', include('board.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
