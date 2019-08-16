# -*- coding: utf-8 -*-
import datetime
import os
import tempfile
from unittest import mock

import pytest
from django.test import TestCase
from django.urls import reverse

from demo.factories import MasterFactory
from demo.serializers import MasterSerializer

from drf_api_checker.exceptions import FieldAddedError, FieldMissedError
from drf_api_checker.recorder import Recorder
from drf_api_checker.unittest import ApiCheckerBase, ApiCheckerMixin


class DemoApi(ApiCheckerMixin):

    def setUp(self):
        super().setUp()
        self.url = reverse("master-list")
        self._base_fields = list(MasterSerializer.Meta.fields)

    def get_fixtures(self):
        return {"master": MasterFactory()}

    def test_a_base(self):
        self.assertGET(self.url)

    def test_a_base_allow_empty(self):
        self.assertGET(self.url, allow_empty=True)

    def test_a_put(self):
        self.url = reverse("master-update", args=[self.get_fixture("master").pk])
        self.assertPUT(self.url, {"name": 'abc',
                                  "capabilities": []})

    def test_a_post(self):
        self.url = reverse("master-create")
        self.assertPOST(self.url, {"name": 'abc',
                                   "capabilities": []})

    def test_a_delete(self):
        self.url = reverse("master-delete", args=[self.get_fixture("master").pk])
        self.assertDELETE(self.url, {"name": 'abc',
                                     "capabilities": []})

    def test_b_remove_field(self):
        self.assertGET(self.url, name='remove_field', check_headers=False)
        os.environ['API_CHECKER_RESET'] = "" # ignore --reset-contracts
        with mock.patch('demo.serializers.MasterSerializer.Meta.fields', ('name',)):
            with pytest.raises(FieldMissedError):
                self.assertGET(self.url, name='remove_field', check_headers=False)

    def test_c_add_field(self):
        self.assertGET(self.url, name='add_field', check_headers=False)
        os.environ['API_CHECKER_RESET'] = "" # ignore --reset-contracts
        with mock.patch('demo.serializers.MasterSerializer.Meta.fields',
                        ('id', 'name', 'alias', 'capabilities', 'timestamp')):
            with pytest.raises(FieldAddedError):
                self.assertGET(self.url, name='add_field', check_headers=False)

    def test_detail(self):
        self.url = reverse("master-detail", args=[self.get_fixture("master").pk])
        self.assertGET(self.url)


class Test1DemoApi(DemoApi, TestCase):
    def assert_timestamp(self, response, expected, path=''):
        value = response['timestamp']
        assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')


class Test2DemoApi(DemoApi, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data_dir = tempfile.mkdtemp()
        cls.recorder = Recorder(cls.data_dir, cls)


class TestUrls(TestCase, metaclass=ApiCheckerBase):
    URLS = [
        reverse("master-list"),
        reverse("master-detail", args=[101]),
    ]

    def get_fixtures(cls):
        return {'master': MasterFactory(id=101)}

    def assert_timestamp(self, response, expected, path=''):
        value = response['timestamp']
        assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
