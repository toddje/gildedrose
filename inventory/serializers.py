# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers


class ItemSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    descriptions = serializers.CharField()
    price = serializers.IntegerField()
    count = serializers.IntegerField()
