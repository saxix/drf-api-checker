import os
import sys
from pathlib import Path

import pytest


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, str(Path(here) / 'demoapp'))


@pytest.fixture(autouse=True)
def setup_recorder(monkeypatch):
    import django

    import drf_api_checker.pytest
    v = ".".join(map(str, django.VERSION[0:2]))
    target = f"_api_checker_{v}"
    monkeypatch.setattr('drf_api_checker.recorder.BASE_DATADIR', target)
    monkeypatch.setattr('drf_api_checker.unittest.BASE_DATADIR', target)
    monkeypatch.setattr('drf_api_checker.pytest.BASE_DATADIR', target)


@pytest.fixture(scope='session')
def client(request):
    import django_webtest

    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


@pytest.fixture
def master(db):
    from demo.factories import MasterFactory
    return MasterFactory()


@pytest.fixture
def detail(master):
    from demo.factories import DetailFactory
    return DetailFactory(master=master)


@pytest.fixture
def masters(db):
    from demo.factories import MasterFactory
    return MasterFactory(), MasterFactory()


@pytest.fixture
def details(db):
    from demo.factories import DetailFactory
    return DetailFactory(), DetailFactory()
