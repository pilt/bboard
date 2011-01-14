# -*- coding: utf-8 -*-
"""
board.admin
~~~~~~~~~~~
Register models the admin site.
"""

from django.db.models import Model
from django.contrib import admin

from board import models

for k, v in models.__dict__.items():
    if isinstance(v, type) and issubclass(v, Model):
        admin.site.register(v)
