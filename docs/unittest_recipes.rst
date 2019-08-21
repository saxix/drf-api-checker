.. include:: globals.txt

.. _unittest_recipes:

Unittest Recipes
================


Check ``DateTimeField()`` with ``auto_now=True``
------------------------------------------------

Add a method ``assert_<fieldname>`` that check by format instead

.. code-block:: python

    class TestUrls(TestCase, metaclass=ApiCheckerBase):

        def assert_timestamp(self, response, expected, path=''):
            value = response['timestamp']
            assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')


Check protected url
-------------------

Using standard DRF way: ``self.client.login()`` or ``self.client.force_authenticate()``

