# -*- coding: utf-8 -*-
import inspect
import os
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


def frozenfixture(func):
    from drf_api_checker.utils import load_fixtures, dump_fixtures
    from drf_api_checker.fs import mktree

    @wraps(func)
    def _inner(*args, **kwargs):
        destination = os.path.join(os.path.dirname(func.__code__.co_filename),
                                   BASE_DATADIR,
                                   func.__module__,
                                   func.__name__,
                                   ) + '.fixture.json'
        if os.path.exists(destination) and not os.environ.get('API_CHECKER_RESET'):
            return load_fixtures(destination)[func.__name__]
        mktree(os.path.dirname(destination))
        data = func(*args, **kwargs)
        dump_fixtures({func.__name__: data}, destination)
        return data

    return pytest.fixture(_inner)


def contract(recorder_class=Recorder, allow_empty=False, headers=True, status=True, name=None, method='get'):
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
            recorder._assertCALL(url, allow_empty=allow_empty,
                                 check_headers=headers,
                                 check_status=status,
                                 name=name, method=method, data=data)
            return True

        return _inner

    return _inner1
