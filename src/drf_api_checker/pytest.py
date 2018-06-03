# -*- coding: utf-8 -*-
import inspect
import os
from functools import wraps

import pytest
from drf_api_checker.recorder import Recorder


def frozenfixture(func):
    from drf_api_checker.unittest import BASE_DATADIR
    from drf_api_checker.utils import load_fixtures, dump_fixtures
    from drf_api_checker.fs import mktree
    destination = os.path.join(os.path.dirname(func.__code__.co_filename),
                               BASE_DATADIR,
                               func.__module__,
                               func.__name__,
                               ) + '.fixture.json'

    @wraps(func)
    def _inner(*args, **kwargs):
        if os.path.exists(destination):
            return load_fixtures(destination)[func.__name__]
        mktree(os.path.dirname(destination))
        data = func(*args, **kwargs)
        dump_fixtures({func.__name__: data}, destination)
        return data

    return pytest.fixture(_inner)


def contract(recorder=Recorder, allow_empty=False, headers=True, status=True, name=None):
    def _inner1(func):
        from drf_api_checker.unittest import BASE_DATADIR
        data_dir = os.path.join(os.path.dirname(inspect.getfile(func)),
                                BASE_DATADIR,
                                func.__module__, func.__name__)

        @wraps(func)
        def _inner(*args, **kwargs):
            url = func(*args, **kwargs)
            recorder = Recorder(data_dir)
            recorder.assertAPI(url, allow_empty, headers, status, name)
            return True

        return _inner

    return _inner1
