# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Forum(models.Model):
    slug = models.SlugField(unique=True, verbose_name=_(u'Slug'))
    title = models.CharField(max_length=255, verbose_name=_(u'Title'))
    description = models.CharField(max_length=1024, verbose_name=_(u'Description'))
    ordering = models.IntegerField(default=0, verbose_name=_(u'Ordering'), db_index=True)
#    closed = models.BooleanField(verbose_name=_(u'Closed'), db_index=True, default=False)

    class Meta:
        ordering = ['ordering',]
        permissions = (("view_forum", "Can view forum"),)

    def __unicode__(self):
        return self.title



class Topic(models.Model):
    forum = models.ForeignKey(Forum)
    subject = models.CharField(verbose_name=_(u'Subject'), max_length=255)
    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name=_(u'Created'))
    public = models.BooleanField(verbose_name=_(u'Publicated'), db_index=True, default=True)
#    closed = models.BooleanField(verbose_name=_(u'Closed'), db_index=True, default=False)

    class Meta:
        ordering = ['-id']
        permissions = (("view_topic", "Can view forum topic"),)


class Article(models.Model):
    topic = models.ForeignKey(Topic)
    author = models.ForeignKey(User, blank=True, null=True, verbose_name=_(u'Author'))
    text = models.TextField(verbose_name=_(u'Text of message'))
    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name=_(u'Created'))
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_(u'Created'))
    public = models.BooleanField(verbose_name=u'Publicated', db_index=True, default=True)

    class Meta:
        ordering = ['created']
        permissions = (("view_article", "Can view forum message"),)

    def __unicode__(self):
        return u'(%s, %s)' % (self.topic, self.author)

