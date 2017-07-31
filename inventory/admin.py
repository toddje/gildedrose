# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


from django.contrib import admin
from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions')

admin.site.register(models.Item, ItemAdmin)
