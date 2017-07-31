Guilded Rose
============

## Setup

 I recommended a dev setup using virtualenv.

 Ensure virtualenv is installed.

```
  $ pip install virtualenv
```

 To set up a virtualenv with python 2.7:

```
  $ cd gildedrose
  $ virtualenv env
  $ source ./env/bin/activate
  $ pip install -r dev_requirements.txt
```

 Initialize the database, configured to use sqlite3

```
  $ python manage.py migrate
```

 Create the super user:

```
  $ python manage.py createsuperuser
```

 Run the dev server

```
  $ python manage.py runserver
```

Visit the django admin site at http://localhost:8000/admin/

Login with the superuser credentials just created.

This admin site will allow the creation of Items, and Users.

Visit the API docs site at http://localhost:8000/docs/.


## Data Formats

I used the Django Rest Framework, which is the most commonly used
library for building REST APIs on a Django project.

### Inventory Items API

I chose to make this API paginated, so that client apps wouldn't be
overwhelmed by large data sets.

The URL looks like http://localhost:8000/api/inventory/items/?page=1&page_size=10

This end point supports GET.

The page size can be controlled by the requesting client.  I chose the
fields that the serializer used for each item.  This is what the data
returned by the API looks like:

```javascript
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
```

The id is key because it is used to identify the item in the purchase
API.  I included all these fields so that the user would be able to
decide which items to purchase.

### Inventory Purchase

The URL looks like http://localhost:8000/api/inventory/item/purchase/


The data posted must be in this format:

```javascript
{"id": 10 }
```

The id value is from the corresponding item in the inventory/items API.

The response from the API will indicate if the purchase was successful
or not.

Success:

```javascript
{"success": true}
```

Failure:

```javascript
{"success": false, "message": "The item is out of stock"}
```


## Authentication

I chose a Basic Auth user-based authentication because in this
situation the store can only sell to users who have set up accounts,
and have a known delivery address, and a way of paying.  All of this
would be associated with their account in a full implementation.

This must be run over https when deployed to protect this information
in the requests.
