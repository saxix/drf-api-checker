# -*- coding: utf-8 -*-
import inspect
import os

from django.test import Client

from drf_api_checker.fs import clean_url, get_filename
from drf_api_checker.recorder import Recorder
from drf_api_checker.utils import dump_fixtures, load_fixtures

BASE_DATADIR = '_api_checker'


class ApiCheckerMixin:
    """
    Mixin to enable API contract check

    How to use it:

    - implement get_fixtures() to create data for test. It should returns a dictionary
    - use self.assertAPI(url) to check urls contract

    Example:

    class TestAPIAgreements(ApiCheckerMixin, TestCase):
        def get_fixtures(self):
            return {'customer': CustomerFactory()}

        def test_customer_detail(self):
            url = reverse("customer-detail", args=[self.get_fixture('customer').pk])
            self.assertAPI(url)

    """
    recorder_class = Recorder

    def setUp(self):
        super().setUp()
        self.client = self.client_class()
        self._process_fixtures()
        self.recorder = self.recorder_class(self.data_dir, self)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data_dir = os.path.join(os.path.dirname(inspect.getfile(cls)),
                                    BASE_DATADIR,
                                    cls.__module__, cls.__name__)

    # def get_response_filename(self, url):
    #     return get_filename(self.data_dir, clean_url(url) + '.response.json')

    def get_fixtures_filename(self, basename='fixtures'):
        return get_filename(self.data_dir, f'{basename}.json')

    def get_fixtures(self):
        """ returns test fixtures.
        Should returns a dictionary where any key is a fixture name
        the value should be a Model instance (or a list).

        {'user' : UserFactory(username='user'),
         'partners': [PartnerFactory(), PartnerFactory()],
        }

        fixtures can be accessed using `get_fixture(<name>)`
        """
        return {}  # pragma: no cover

    def get_fixture(self, name):
        """
        returns fixture `name` loaded by `get_fixtures()`
        """
        return self.__fixtures[name]  # pragma: no cover

    def _process_fixtures(self):
        """ store or retrieve test fixtures """
        fname = self.get_fixtures_filename()
        if os.path.exists(fname):
            self.__fixtures = load_fixtures(fname)
        else:
            self.__fixtures = self.get_fixtures()
            if self.__fixtures:
                dump_fixtures(self.__fixtures, fname)

    def assertAPI(self, url, allow_empty=False, check_headers=True, check_status=True, name=None):
        self.recorder.assertAPI(url, allow_empty, check_headers, check_status, name)


class ApiCheckerBase(type):
    """
Custom _type_, intended to be used as metaclass.
It will create a test for each url defined in URLS in the format
`test__<normalized_url_path>`,  if a method with the same name is found the
creation is skipped reading this as an intention to have a custom test for that url.

    class TestAPIIntervention(TestCase, metaclass=ApiCheckerBase):
        URLS = [
                reverse("intervention-list"),
                reverse("intervention-detail", args=[101]),
               ]
        def get_fixtures(cls):
            return {'intervention': InterventionFactory(id=101),
               'result': ResultFactory(),
               }

running this code will produce...

...
test_url__api_v2_interventions (etools.applications.partners.tests.test_api.TestAPIIntervention) ... ok
test_url__api_v2_interventions_101 (etools.applications.partners.tests.test_api.TestAPIIntervention) ... ok
...

    """
    mixin = ApiCheckerMixin

    def __new__(cls, clsname, superclasses, attributedict):
        superclasses = (cls.mixin,) + superclasses
        clazz = type.__new__(cls, clsname, superclasses, attributedict)

        def check_url(url):
            def _inner(self):
                self.assertAPI(url)

            _inner.__name__ = "test_url__" + clean_url(u)
            return _inner

        if 'URLS' not in attributedict:  # pragma: no cover
            raise ValueError(f"Error creatine {clsname}. "
                             f"ApiCheckerBase requires URLS attribute ")

        for u in attributedict['URLS']:
            m = check_url(u)
            if not hasattr(clazz, m.__name__):
                setattr(clazz, m.__name__, m)

        return clazz
