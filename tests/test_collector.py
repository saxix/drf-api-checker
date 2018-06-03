# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest

from drf_api_checker.collector import ForeignKeysCollector


@pytest.mark.django_db(transaction=False)
def test_collect_single(detail):
    collector = ForeignKeysCollector(None)
    collector.collect(detail)
    assert collector.data == [detail, detail.master]


@pytest.mark.django_db(transaction=False)
def test_collect_duplicate(detail):
    collector = ForeignKeysCollector(None)
    collector.collect([detail, detail.master])
    assert collector.data == [detail, detail.master]


@pytest.mark.django_db(transaction=False)
def test_collect_multiple(detail, masters):
    m1, m2 = masters
    collector = ForeignKeysCollector(None)
    collector.collect([detail, m1, m2])
    assert collector.data == [detail, detail.master, m1, m2]
