# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import views
urlpatterns = patterns(views,
    url(r'^$', views.forums , name="forums"),
    url(r'^article_delete/(?P<id>\d+)/$', views.article_delete , name="article_delete"),
    url(r'^article_hide/(?P<id>\d+)/$', views.article_hide , name="article_hide"),
    url(r'^article_show/(?P<id>\d+)/$', views.article_show , name="article_show"),
    url(r'^topic_delete/(?P<id>\d+)/$', views.topic_delete , name="topic_delete"),
    url(r'^topic_open/(?P<id>\d+)/$', views.topic_open , name="topic_open"),
    url(r'^topic_close/(?P<id>\d+)/$', views.topic_close , name="topic_close"),
    url(r'^forum_delete/(?P<id>\d+)/$', views.forum_delete , name="forum_delete"),

    url(r'^article_preview/$', views.article_preview , name="article_preview"),

    url(r'^(?P<slug>[_-w]+)/$', views.forum_topics , name="topics"),
    url(r'^(?P<slug>[_-w]+)/(?P<id>\d+)/$', views.topic_articles , name="articles"),
    url(r'^(?P<slug>[_-w]+)/(?P<id>\d+)/replay/(?P<aid>\d+)/$', views.topic_articles , name="replay_article"),
    url(r'^(?P<slug>[_-w]+)/(?P<id>\d+)/edit/(?P<eid>\d+)/$', views.topic_articles , name="edit_article"),
#    url(r'^(?P<slug>[_-a-z0-9]+)/(?P<id>\d+)/$', views.show , name="show_topic"),
)
