import os
import sys
from pathlib import Path

import pytest


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, str(Path(here) / "demoapp"))


@pytest.fixture(scope="session")
def client(request):
    import django_webtest  # noqa

    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)  # noqa
    return django_webtest.DjangoTestApp()


@pytest.fixture
def master(db):
    from demo.factories import MasterFactory  # noqa

    return MasterFactory()


@pytest.fixture
def detail(master):
    from demo.factories import DetailFactory  # noqa

    return DetailFactory(master=master)


@pytest.fixture
def masters(db):
    from demo.factories import MasterFactory  # noqa

    return MasterFactory(), MasterFactory()


@pytest.fixture
def details(db):
    from demo.factories import DetailFactory  # noqa

    return DetailFactory(), DetailFactory()
