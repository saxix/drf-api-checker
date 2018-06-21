.. include:: globals.txt
.. _recipes:

Common Recipes
===============


Check ``DateTimeField()`` with ``auto_now=True``
----------------------------------------------

**Using Django TestCase:**

Add a method ``assert_<fieldname>`` that check by format instead

.. code-block:: python

    class TestUrls(TestCase, metaclass=ApiCheckerBase):

        def assert_timestamp(self, response, expected, path=''):
            value = response['timestamp']
            assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')

**With pytest:**


Create a custom :ref:`Recorder` and pass it to :ref:`contract`


.. code-block:: python

    from drf_api_checker.recorder import Recorder
    from drf_api_checker.pytest import contract, frozenfixture

    class MyRecorder(Recorder):

        def assert_timestamp(self, response, expected, path=''):
            value = response['timestamp']
            assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')


    @contract(recorder_class=MyRecorder)
    def test_user_list(user):
        return reverse('api:user-list')


Check protected url
-------------------

**Using Django TestCase:**

Using standard DRF way: ``self.client.login()`` or ``self.client.force_authenticate()``

**With pytest:**

Create a custom :ref:`Recorder` and override ``client`` property


.. code-block:: python

    class MyRecorder(Recorder):
        @property
        def client(self):
            user = UserFactory(is_superuser=True)
            client = APIClient()
            client.force_authenticate(user)
            return client

    @contract(recorder_class=MyRecorder)
    def test_user_list(user):
        return reverse('api:user-list')



Check methods other than GET
----------------------------

.. code-block:: python

    from drf_api_checker.recorder import Recorder
    from drf_api_checker.pytest import contract, frozenfixture


