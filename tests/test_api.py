# -*- coding: utf-8 -*-
import datetime
import tempfile
from unittest import mock

import pytest
from django.test import TestCase
from django.urls import reverse

from demo.factories import MasterFactory
from demo.serializers import MasterSerializer
from drf_api_checker.unittest import ApiCheckerMixin, ApiCheckerBase
from drf_api_checker.exceptions import FieldMissedError, FieldAddedError
from drf_api_checker.recorder import Recorder


class DemoApi(ApiCheckerMixin):

    def setUp(self):
        super().setUp()
        self.url = reverse("master-list")
        self._base_fields = list(MasterSerializer.Meta.fields)

    def get_fixtures(self):
        return {"master": MasterFactory()}

    def test_a_base(self):
        self.assertAPI(self.url)

    def test_b_remove_field(self):
        with mock.patch('demo.serializers.MasterSerializer.Meta.fields', ('name',)):
            with pytest.raises(FieldMissedError):
                self.assertAPI(self.url)

    def test_c_add_field(self):
        with mock.patch('demo.serializers.MasterSerializer.Meta.fields',
                        ('id', 'name', 'alias', 'capabilities', 'timestamp')):
            with pytest.raises(FieldAddedError):
                self.assertAPI(self.url)

    def test_detail(self):
        self.url = reverse("master-detail", args=[self.get_fixture("master").pk])
        self.assertAPI(self.url)


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
