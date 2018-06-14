.. include:: globals.txt
.. _index:

===============================
DjangoRestFramework API checker
===============================

Overview
========

.. image:: https://img.shields.io/travis/saxix/drf-api-checker/master.svg
    :target: http://travis-ci.org/saxix/drf-api-checker/
    :alt: Test status

.. image:: https://codecov.io/github/saxix/drf-api-checker/coverage.svg?branch=master
    :target: https://codecov.io/github/saxix/drf-api-checker?branch=master
    :alt: Coverage




This module offers some utilities to avoid unwanted changes in Django Rest Framework responses,
so to keep stable contracts

The purpose is to guarantee that any code changes never introduce 'contract violations'
changing the Serialization behaviour.


Contract violations can happen when:

- fields are removed from Serializer
- field representation changes (ie. date/number format, )
- Response status code changes (optional)
- Response headers change (optional)


How it works:
-------------

First time the test is ran, the response and model instances are serialized and
saved on the disk; any further execution is checked against this first response.

Test data are saved in the same directory where the test module lives,
under ``_api_checker/<module_fqn>/<test_class>``

Fields that cannot be checked by value (ie timestamps/last modified) can be tested writing
custom ``assert_<field_name>`` methods.

In case of nested objects, method names must follow the field "path".
(ie. ``assert_permission_modified`` vs ``assert_modified``)

This module can also intercept when a field is added,
in this case it is mandatory recreate stored test data; simply delete them from the disk
or set ``API_CHECKER_RESET`` environment variable and run the test again,



In case something goes wrong the output will be


**Field values mismatch**


.. code-block:: bash


    AssertionError: View `<class 'path.to.module.CustomerListAPIView>` breaks the contract.
    Field `name` does not match.
    - expected: `Partner 0`
    - received: `Partner 11`


**Field removed**

.. code-block:: bash


    AssertionError: View `<class 'path.to.module.CustomerListAPIView'>` breaks the contract.
    Field `id` is missing in the new response


**Field added**


.. code-block:: bash


    AssertionError: View `<class 'path.to.module.CustomerListAPIView'>` returned more field than expected.
    Action needed api_customers.response.json need rebuild.
    New fields are:
    `['country']`



Content
=======

Support for django test is provided by:

    - :ref:`ApiCheckerMixin`
    - :ref:`ApiCheckerBase`

pytest is supported via decorators:

    - :ref:`frozenfixture`
    - :ref:`contract`




Table Of Contents
=================

.. toctree::
    :maxdepth: 1

    install
    howto
    recipes
    api


Links
=====

   * Project home page: https://github.com/saxix/drf-api-checker
   * Issue tracker: https://github.com/saxix/drf-api-checker/issues?sort
   * Download: http://pypi.python.org/pypi/drf-api-checker/
   * Docs: http://readthedocs.org/docs/drf-api-checker/en/latest/
