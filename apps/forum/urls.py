# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('forum.frontend.urls', namespace='frontend')),
#    (r'^admin/', include('forum.administration.urls', namespace='administration')),
)

