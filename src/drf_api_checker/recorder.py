# -*- coding: utf-8 -*-
import os

from django.test import Client
from django.urls import resolve

from drf_api_checker.exceptions import FieldAddedError, FieldMissedError, FieldValueError, StatusCodeError
from drf_api_checker.fs import clean_url, get_filename
from drf_api_checker.utils import _write, load_response, serialize_response

OVEWRITE = os.environ.get('API_CHECKER_RESET', False)


class Recorder:

    def __init__(self, data_dir, owner=None) -> None:
        self.data_dir = data_dir
        self.owner = owner

    @property
    def client(self):
        if self.owner:
            return self.owner.client
        else:
            return Client()

    def get_response_filename(self, url):
        return get_filename(self.data_dir, clean_url(url) + '.response.json')

    def _compare_dict(self, response, stored, path='', view='unknown'):
        for field_name, v in response.items():
            if isinstance(v, dict):
                self._compare_dict(v, stored[field_name], f"{path}_{field_name}", view=view)
            else:
                if hasattr(self, f'assert_{path or field_name}'):
                    asserter = getattr(self, f'assert_{path or field_name}')
                    asserter(response, stored, path)
                elif hasattr(self.owner, f'assert_{path or field_name}'):
                    asserter = getattr(self.owner, f'assert_{path or field_name}')
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
        _recv = set(response.keys())
        _expct = set(expected.keys())
        added = _recv.difference(_expct)
        missed = _expct.difference(_recv)

        if missed:
            raise FieldMissedError(view, ", ".join(missed))
        if added:
            raise FieldAddedError(view, ", ".join(added), filename)
        self._compare_dict(response, expected, view=view)

    def assertAPI(self, url, allow_empty=False, check_headers=True, check_status=True, expect_errors=False, name=None):
        """
        check url for response changes

        :param url: url to check
        :param allow_empty: if True ignore empty response and 404 errors
        :param check_headers: check response headers
        :param check_status: check response status code
        :raises: ValueError
        :raises: AssertionError
        """
        view = resolve(url).func.cls

        filename = self.get_response_filename(name or url)
        response = self.client.get(url)
        assert response.accepted_renderer
        payload = response.data
        if not allow_empty and not payload:
            raise ValueError(f"View {view} returned and empty json. Check your test")

        if response.status_code > 299 and not expect_errors:
            raise ValueError(f"View {view} unexpected response. {response.status_code} - {response.content}")

        if not allow_empty and response.status_code == 404:
            raise ValueError(f"View {view} returned 404 status code. Check your test")

        if not os.path.exists(filename) or OVEWRITE:
            _write(filename, serialize_response(response))

        stored = load_response(filename)
        if (check_status) and response.status_code != stored.status_code:
            raise StatusCodeError(view, response.status_code, stored.status_code)
        if check_headers:
            self._assert_headers(response, stored)
        self.compare(payload, stored.data, filename, view=view)

    def _assert_headers(self, response, stored):
        assert response['Content-Type'] == stored['Content-Type']
        assert sorted(response['Allow']) == sorted(stored['Allow'])
