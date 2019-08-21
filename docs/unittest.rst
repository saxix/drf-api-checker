.. include:: globals.txt

.. _unittest:

Unitest style test support
==========================

Unitest style is supported via  :ref:`ApiCheckerMixin` and :ref:`ApiCheckerBase`

ApiCheckerMixin
---------------

Base test looks like::

    class TestAPIAgreements(ApiCheckerMixin, TestCase):
        def get_fixtures(self):
            return {'customer': CustomerFactory()}

        def test_customer_detail(self):
            url = reverse("customer-detail", args=[self.get_fixture('customer').pk])
            self.assertGET(url)

``get_fixtures`` must returns a dictionary of all the fixtures that need to be restored to
have comparable responses.

**WARNING**: when `factory_boy`_ is used pay attention to ForeignKeys. They need to be listed too
and the factory need to be written in a way that can reproduce predictable records


ApiCheckerBase
--------------

.. code-block:: python

    class TestAPIIntervention(TestCase, metaclass=ApiCheckerBase):
        URLS = [
                reverse("intervention-list"),
                reverse("intervention-detail", args=[101]),
               ]

        def get_fixtures(cls):
            return {'intervention': InterventionFactory(id=101),
               'result': ResultFactory(),
               }
