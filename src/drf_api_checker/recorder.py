# -*- coding: utf-8 -*-
import os

from django.urls import resolve

from drf_api_checker.exceptions import (
    FieldAddedError, FieldMissedError, FieldValueError, HeaderError, StatusCodeError
)
from drf_api_checker.fs import clean_url, get_filename
from drf_api_checker.utils import _write, load_response, serialize_response

HEADERS_TO_CHECK = ['Content-Type', 'Content-Length', 'Allow']
BASE_DATADIR = '_api_checker'

STATUS_CODE = 1
FIELDS = 2
HEADERS = 3
DEFAULT_CHECKS = [STATUS_CODE, FIELDS, HEADERS]


class Recorder:
    expect_errors = False
    allow_empty = False
    headers = HEADERS_TO_CHECK
    checks = list(DEFAULT_CHECKS)

    def __init__(self, data_dir, owner=None, headers_to_check=None) -> None:
        self.data_dir = data_dir
        self.owner = owner
        self.headers_to_check = headers_to_check or self.headers
        self.check_map = {FIELDS: self._assert_fields,
                          STATUS_CODE: self._assert_status,
                          HEADERS: self._assert_headers
                          }
        # self._checks = [check_map[i] for i in self.checks]
        # self.check_headers = HEADERS in check_map
        # self.check_status = STATUS_CODE in check_map
        if hasattr(self, 'check_headers'):
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'checks' instead.")
        if hasattr(self, 'check_status'):
            raise DeprecationWarning("'check_status' has been deprecated. Use 'checks' instead.")

    @property
    def client(self):
        if self.owner:
            return self.owner.client
        else:
            from rest_framework.test import APIClient
            return APIClient()

    def get_response_filename(self, method, url, data):
        return get_filename(self.data_dir, clean_url(method, url, data) + '.response.json')

    def _get_custom_asserter(self, path, field_name):
        for attr in [f'assert_{path}_{field_name}', f'assert_{field_name}']:
            for target in [self, self.owner]:
                if hasattr(target, attr):
                    return getattr(target, attr)
        return None

    def _compare_dict(self, response, stored, path='', view='unknown'):
        for field_name, v in response.items():
            if isinstance(v, dict):
                self._compare_dict(v, stored[field_name], f"{path}_{field_name}", view=view)
            else:
                asserter = self._get_custom_asserter(path, field_name)
                if asserter:
                    asserter(response, stored, path)
                else:
                    if isinstance(v, set):
                        v = list(v)

                    if field_name in stored and v != stored[field_name]:
                        raise FieldValueError(view=view,
                                              expected=stored[field_name],
                                              receiced=response[field_name],
                                              field_name=field_name,
                                              filename=self.data_dir)

    def compare(self, response, expected, filename='unknown', ignore_fields=None, view='unknown'):
        if isinstance(response, (list, tuple)):
            response = response[0]
            expected = expected[0]
        if response:
            _recv = set(response.keys())
            _expct = set(expected.keys())
            added = _recv.difference(_expct)
            missed = _expct.difference(_recv)

            if missed:
                raise FieldMissedError(view, ", ".join(missed))
            if added:
                raise FieldAddedError(view, ", ".join(added), filename)
            self._compare_dict(response, expected, view=view)
        else:
            assert response == expected

    def assertGET(self, url, *, allow_empty=None, targets=None,
                  expect_errors=None, name=None, data=None, **kwargs):
        if 'check_headers' in kwargs:
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'targets' instead.")
        if 'check_status' in kwargs:
            raise DeprecationWarning("'check_status' has been deprecated. Use 'targets' instead.")
        if kwargs:
            raise AttributeError("Unknown arguments %s" % kwargs.keys())
        self.assertCALL(url, allow_empty=allow_empty,
                        targets=targets,
                        expect_errors=expect_errors, name=name, data=data)

    def assertPUT(self, url, data, *, allow_empty=None,
                  expect_errors=None, name=None, targets=None, **kwargs):
        if 'check_headers' in kwargs:
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'targets' instead.")
        if 'check_status' in kwargs:
            raise DeprecationWarning("'check_status' has been deprecated. Use 'targets' instead.")
        if kwargs:
            raise AttributeError("Unknown arguments %s" % kwargs.keys())
        self.assertCALL(url, data=data, method='put', allow_empty=allow_empty,
                        targets=targets,
                        expect_errors=expect_errors, name=name)

    def assertPOST(self, url, data, *, allow_empty=None, check_headers=None, check_status=None,
                   expect_errors=None, name=None, checks=None, **kwargs):
        if 'check_headers' in kwargs:
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'checks' instead.")
        if 'check_status' in kwargs:
            raise DeprecationWarning("'check_status' has been deprecated. Use 'checks' instead.")
        if kwargs:
            raise AttributeError("Unknown arguments %s" % kwargs.keys())
        self.assertCALL(url, data=data, method='post', allow_empty=allow_empty,
                        check_headers=check_headers, check_status=check_status,
                        expect_errors=expect_errors, name=name)

    def assertDELETE(self, url, *, allow_empty=None,
                     expect_errors=None, name=None, data=None, **kwargs):
        if 'check_headers' in kwargs:
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'checks' instead.")
        if 'check_status' in kwargs:
            raise DeprecationWarning("'check_status' has been deprecated. Use 'checks' instead.")
        if kwargs:
            raise AttributeError("Unknown arguments %s" % kwargs.keys())
        self.assertCALL(url, method='delete', allow_empty=allow_empty,
                        expect_errors=expect_errors, name=name, data=data)

    def assertCALL(self, url, *, allow_empty=None,
                   expect_errors=None, name=None, method='get', data=None,
                   checks=None, **kwargs):
        """
        check url for response changes

        :param url: url to check
        :param allow_empty: if True ignore empty response and 404 errors
        :param checks: list and order checks. ie. `checks=[STATUS_CODE, FIELDS, HEADERS]`
        :param check_status: check response status code
        :raises: ValueError
        :raises: AssertionError
        """
        if 'check_headers' in kwargs:
            raise DeprecationWarning("'check_headers' has been deprecated. Use 'checks' instead.")
        if 'check_status' in kwargs:
            raise DeprecationWarning("'check_status' has been deprecated. Use 'checks' instead.")
        if kwargs:
            raise AttributeError("Unknown arguments %s" % kwargs.keys())

        expect_errors = self.expect_errors if expect_errors is None else expect_errors
        allow_empty = self.allow_empty if allow_empty is None else allow_empty

        self.view = resolve(url).func.cls
        m = getattr(self.client, method.lower())
        self.filename = self.get_response_filename(method, name or url, data)
        response = m(url, data=data)
        assert response.accepted_renderer
        payload = response.data
        if not allow_empty and not payload:
            raise ValueError(f"View {self.view} returned and empty json. Check your test")

        if response.status_code > 299 and not expect_errors:
            raise ValueError(f"View {self.view} unexpected response. {response.status_code} - {response.content}")

        if not allow_empty and response.status_code == 404:
            raise ValueError(f"View {self.view} returned 404 status code. Check your test")

        if not os.path.exists(self.filename) or os.environ.get('API_CHECKER_RESET', False):
            _write(self.filename, serialize_response(response))

        stored = load_response(self.filename)
        if checks is None:
            checks = self.checks
        for check_id in checks:
            check = self.check_map[check_id]
            check(response, stored)

    def _assert_fields(self, response, stored):
        self.compare(response.data, stored.data, self.filename, view=self.view)

    def _assert_status(self, response, stored):
        if response.status_code != stored.status_code:
            raise StatusCodeError(self.view, response.status_code, stored.status_code)

    def _assert_headers(self, response, stored):

        for h in self.headers_to_check:
            _expected = stored.get(h)
            _recv = response.get(h)
            if _expected != _recv:
                raise HeaderError(self.view, h, _expected,
                                  _recv,
                                  self.filename,
                                  f"{stored.content}/{response.content}")

        # if sorted(response.get('Allow')) != sorted(stored.get('Allow')):
        #     raise HeaderError(self.view, h, stored.get(h),
        #                       response.get(h),
        #                       self.filename)
        #
        # assert response.get('Content-Type') == stored.get('Content-Type')
        # assert response.get('Content-Length') == stored.get('Content-Length'), response.content
        # assert sorted(response.get('Allow')) == sorted(stored.get('Allow'))
