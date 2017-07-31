# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from inventory.models import Item
from inventory.serializers import ItemSerializer

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


class ItemView(generics.ListAPIView):
    """
    get:
       Return a list of all the Items, paged, with next/previous links

    Example:
    [
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
    {
      "id": 1,
      "name": "test item 1",
      "descriptions": "This is the first test item",
      "price": 10,
      "count": 10
    },
    {
      "id": 2,
      "name": "Test Item",
      "descriptions": "This is the 2nd Test item",
      "price": 10,
      "count": 10
    }
  ]

    """

    serializer_class = ItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Item.objects.all().order_by('id')


class PurchaseView(APIView):
    """
    post:
       receives the id of an item to buy.
       Returns:
       {"success": true} if purchase succeeds
       {"success": false, "messages":"" } is purchase fails
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        data = request.data
        if 'id' not in data:
            return Response({"message": "No id in request"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            item_id = int(data['id'])
        except:
            return Response({"message": "id not integer"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"message": "Requested item does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)

        if item.purchase():
            resp_data = {"success": True}
        else:
            resp_data = {"success": False,
                         "message": "No inventory"}

        return Response(resp_data,
                        status=status.HTTP_200_OK)
