# -*- coding: utf-8 -*-
"""
board.models
~~~~~~~~~~~~
The convention for remote ids is to name them "rid".
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

class Entry(models.Model):
    rid = models.BigIntegerField(_("remote id"), unique=True)
    title = models.CharField(_("title"), max_length=200)
    mail = models.EmailField(_("email address of the poster"))
    submitted = models.DateTimeField(_("submitted at"))
    body = models.TextField(_("body of the entry"))
    category = models.ForeignKey('board.Category', verbose_name=_("category"))

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __unicode__(self):
        return self.title


class Category(models.Model):
    rid = models.BigIntegerField(_("remote id"), unique=True)
    title = models.CharField(_("title"), max_length=200)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.title


class Search(models.Model):
    term = models.CharField(_("term"), unique=True, max_length=200)
    hit_count = models.IntegerField(_("hit count"), default=0)
    when = models.DateTimeField(_("when"), auto_now_add=True, auto_now=True)

    class Meta:
        verbose_name = _('search')
        verbose_name_plural = _('searches')

    def __unicode__(self):
        return self.term
