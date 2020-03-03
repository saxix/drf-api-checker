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


@pytest.fixture()
def api_checker_datadir(request):
    return get_data_dir(request.function)


def default_fixture_name(seed, request):
    return seed + '.fixture.json'


def frozenfixture(fixture_name=default_fixture_name, is_fixture=True):
    def deco(func):
        from drf_api_checker.utils import load_fixtures, dump_fixtures
        from drf_api_checker.fs import mktree

        @wraps(func)
        def _inner(*args, **kwargs):
            if is_fixture and 'request' not in kwargs:
                raise ValueError('frozenfixture must have `request` argument')
            request = kwargs.get('request', None)
            parts = [os.path.dirname(func.__code__.co_filename),
                     BASE_DATADIR,
                     func.__module__,
                     func.__name__]
            seed = os.path.join(*parts)
            destination = fixture_name(seed, request)

            if not os.path.exists(destination) or os.environ.get('API_CHECKER_RESET'):
                mktree(os.path.dirname(destination))
                data = func(*args, **kwargs)
                dump_fixtures({func.__name__: data}, destination)
            return load_fixtures(destination)[func.__name__]

        if is_fixture:
            return pytest.fixture(_inner)
        return _inner

    return deco


def get_data_dir(func):
    return os.path.join(os.path.dirname(inspect.getfile(func)),
                        BASE_DATADIR,
                        func.__module__, func.__name__)


def contract(recorder_class=Recorder, allow_empty=False, name=None, method='get', checks=None, debug=False, **kwargs):
    if kwargs:
        raise AttributeError("Unknown arguments %s" % ",".join(kwargs.keys()))

    def _inner1(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            data_dir = get_data_dir(func)
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
