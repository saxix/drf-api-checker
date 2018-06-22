.. include:: globals.txt

.. _api:

===
API
===


.. contents::
    :local:



Unittest/django support
=======================


.. _ApiCheckerMixin:

ApiCheckerMixin
---------------

.. autoclass:: drf_api_checker.unittest.ApiCheckerMixin


.. _ApiCheckerBase:

ApiCheckerBase
---------------

.. autoclass:: drf_api_checker.unittest.ApiCheckerBase


pytest support
==============

.. _frozenfixture:

@frozenfixture
---------------

.. autofunction:: drf_api_checker.pytest.frozenfixture



.. _contract:

@contract
---------

.. autofunction:: drf_api_checker.pytest.contract


Internals
=========


.. _Recorder:

Recorder
--------

.. autoclass:: drf_api_checker.recorder.Recorder



.. _ForeignKeysCollector:

ForeignKeysCollector
--------------------

.. autoclass:: drf_api_checker.collector.ForeignKeysCollector
