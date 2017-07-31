# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import handlers

urlpatterns = [
    url(r'^items/$',
        handlers.ItemView.as_view(),
        name='inventory_items'),

    url(r'^item/purchase/$',
        handlers.PurchaseView.as_view(),
        name='item_purchase'),
]
