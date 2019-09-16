# -*- coding: utf-8 -*-
import inspect
import json
import os
import sys
from functools import wraps

import pytest

from drf_api_checker.recorder import BASE_DATADIR, Recorder


def pytest_addoption(parser):
    group = parser.getgroup('DRF API Checker')
    group._addoption('--reset-contracts',
                     action='store_true', dest='reset_contracts', default=False,
                     help='Re-creates all API checker contracts ')


@pytest.fixture(autouse=True, scope="session")
def configure_env(request):
    option = False
    if hasattr(pytest, 'config'):
        option = pytest.config.option.reset_contracts
    elif hasattr(request, 'config'):
        option = request.config.option.reset_contracts

    if option:
        os.environ['API_CHECKER_RESET'] = "1"


def default_fixture_name(seed, request):
    return seed + '.fixture.json'


def frozenfixture(fixture_name=default_fixture_name):
    def deco(func):
        from drf_api_checker.utils import load_fixtures, dump_fixtures
        from drf_api_checker.fs import mktree

        @wraps(func)
        def _inner(*args, **kwargs):
            if 'request' not in kwargs:
                raise ValueError('frozenfixture must have `request` argument')
            request = kwargs['request']
            parts = [os.path.dirname(func.__code__.co_filename),
                     BASE_DATADIR,
                     func.__module__,
                     func.__name__]
            # for x in (fixture_names or []):
            #     if callable(x):
            #         part = x(request)
            #     else:
            #         part = request.getfixturevalue(x)
            #     parts.append(part.__name__)
            #
            # destination = os.path.join(*parts) + '.fixture.json'
            seed = os.path.join(*parts)
            destination = fixture_name(seed, request)

            if not os.path.exists(destination) or os.environ.get('API_CHECKER_RESET'):
                mktree(os.path.dirname(destination))
                data = func(*args, **kwargs)
                dump_fixtures({func.__name__: data}, destination)
            return load_fixtures(destination)[func.__name__]

        return pytest.fixture(_inner)

    return deco


def contract(recorder_class=Recorder, allow_empty=False, name=None, method='get', checks=None, debug=False, **kwargs):
    if 'headers' in kwargs:
        raise DeprecationWarning("'check_headers' has been deprecated. Use 'checks' instead.")
    if 'status' in kwargs:
        raise DeprecationWarning("'check_status' has been deprecated. Use 'checks' instead.")
    if kwargs:
        raise AttributeError("Unknown arguments %s" % ",".join(kwargs.keys()))

    def _inner1(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            data_dir = os.path.join(os.path.dirname(inspect.getfile(func)),
                                    BASE_DATADIR,
                                    func.__module__, func.__name__)

            data = None
            url = func(*args, **kwargs)
            if isinstance(url, (list, tuple)):
                url, data = url
            recorder = recorder_class(data_dir)
            current, contract = recorder.assertCALL(url, allow_empty=allow_empty,
                                                    checks=checks,
                                                    name=name, method=method, data=data)
            if debug:
                sys.stderr.write("Current Response\n")
                sys.stderr.write(json.dumps(current.data, indent=4, sort_keys=True))
                sys.stderr.write("Expected Response\n")
                sys.stderr.write(json.dumps(contract.data, indent=4, sort_keys=True))

            return True

        return _inner

    return _inner1
