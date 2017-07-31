# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models


class Item(models.Model):
    name = models.TextField(default="")
    descriptions = models.TextField(default="")
    price = models.IntegerField(default=0)
    count = models.PositiveIntegerField(default=0)

    def purchase(self):
        # Make sure there's an item
        if self.count > 0:
            self.count -= 1
            self.save()
            return True
        else:
            return False
