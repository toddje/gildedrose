# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer

from model_mommy import mommy

import simplejson as json
import base64

from .models import Item
from .serializers import ItemSerializer


class TestData(TestCase):

    def setUp(self):
        mommy.make('inventory.Item', _quantity=4)

    def test_serializer(self):
        # Make sure serialzer puts correct data into it's output
        s = ItemSerializer(Item.objects.all(),
                           many=True)

        self.assertEqual(4, len(s.data))
        data = JSONRenderer().render(s.data)
        data = json.loads(data)
        i1 = data[0]

        for k in ['id', 'name', 'descriptions', 'price', 'count']:
            self.assertTrue(k in i1)

        self.assertEqual(5, len(i1.keys()))


class TestItem(TestCase):

    def setUp(self):
        mommy.make('inventory.Item', count=1)

    def test_purchase(self):
        item = Item.objects.all().order_by('id')[0]
        # purchase the 1 item successfully
        self.assertEqual(item.count, 1)
        self.assertTrue(item.purchase())
        self.assertEqual(item.count, 0)

        # try to purchase item when 0 count and fail
        self.assertFalse(item.purchase())
        self.assertEqual(item.count, 0)


class TestInventoryAPI(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_one(self):
        mommy.make('inventory.Item', _quantity=4)

        # Ensure the inventory API returns the correct number of items
        self.assertEqual(Item.objects.all().count(), 4)

        url = reverse('api:inventory_items')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        items = data['results']
        self.assertEqual(4, len(items))

    def test_page(self):
        # create 100 items
        mommy.make('inventory.Item', _quantity=100)

        # get first page
        url = reverse('api:inventory_items')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)

        items1 = data['results']
        self.assertEqual(10, len(items1))

        # use data link url to next page
        url = data['next']
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        items2 = data['results']
        self.assertEqual(10, len(items2))

        self.assertNotEqual(items1, items2)


class TestPurchaseAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test',
                                             'test@example.com',
                                             'test')

        credentials = base64.b64encode('test:test')
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials

    def tearDown(self):
        pass

    def test_purchase(self):
        # purchase succeeds when inventory is > 0
        mommy.make('inventory.Item', _quantity=4, count=10)
        item = Item.objects.all().order_by('id')[0]

        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'id': item.id})

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertTrue(data['success'])

    def test_purchase_fail(self):
        # purchase fails when inventory is 0

        mommy.make('inventory.Item', count=0)
        item = Item.objects.all().order_by('id')[0]

        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'id': item.id})
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertFalse(data['success'])

    def test_purchase_bad_id(self):
        # purchase fails when inventory is 0

        mommy.make('inventory.Item', count=10)

        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'id': "alpha"})
        self.assertEqual(resp.status_code, 400)

    def test_purchase_no_id(self):
        # purchase fails when inventory is 0

        mommy.make('inventory.Item', count=10)
        item = Item.objects.all().order_by('id')[0]
        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'item': item.id})
        self.assertEqual(resp.status_code, 400)


class TestPurchaseFailAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test',
                                             'test@example.com',
                                             'test')

        credentials = base64.b64encode('test:test')
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Basic ' + credentials

    def tearDown(self):
        pass

    def test_no_inventory_purchase(self):
        # purchase succeeds when inventory is > 0
        mommy.make('inventory.Item', _quantity=4, count=0)
        item = Item.objects.all().order_by('id')[0]

        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'id': item.id})

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertFalse(data['success'])


class TestPurchaseFailNoAuthAPI(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_no_valid_auth(self):
        # purchase succeeds when inventory is > 0
        mommy.make('inventory.Item', _quantity=4, count=0)
        item = Item.objects.all().order_by('id')[0]

        url = reverse('api:item_purchase')

        resp = self.client.post(url, {'id': item.id})

        self.assertEqual(resp.status_code, 401)
