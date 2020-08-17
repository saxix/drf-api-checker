# DRF API Checker


[![pypi-version]][pypi] 
[![travis-png-m]][travis-l-m] 
[![rtd-badge]][rtd-link]
[![codecov-badge]][codecov]


This module offers some utilities to avoid unwanted changes in Django Rest Framework responses,
so to keep stable contracts

The purpose is to guarantee that any code changes never introduce 'contract violations'
changing the Serialization behaviour.


Contract violations can happen when:

- fields are removed from Serializer
- field representation changes (ie. date/number format, )
- Response status code changes (optional check)
- Response headers change (optional check)


How it works:
-------------

First time the test run, the response and model instances are serialized and
saved on the disk; any further execution is checked against this first response.

Test data are saved in the same directory where the test module lives,
under `_api_checker/<module_fqn>/<test_class>`

Fields that cannot be checked by value (ie timestamps/last modified) can be tested writing
custom `assert_<field_name>` methods.

In case of nested objects, method names must follow the field "path".
(ie. `assert_permission_modified` vs `assert_modified`)

This module can also intercept when a field is added,
in this case it is mandatory recreate stored test data; simply delete them from the disk
or set `API_CHECKER_RESET` environment variable and run the test again,


in case something goes wrong the output will be

**Field values mismatch**

    AssertionError: View `<class 'path.to.module.CustomerListAPIView'>` breaks the contract.
    Field `name` does not match.
    - expected: `Partner 0`
    - received: `Partner 11`


**Field removed**

    AssertionError: View `<class 'path.to.module.CustomerListAPIView'>` breaks the contract.
    Field `id` is missing in the new response


**Field added**

    AssertionError: View `<class 'path.to.module.CustomerListAPIView'>` returned more field than expected.
    Action needed api_customers.response.json need rebuild.
    New fields are:
    `['country']`


How To use it:
--------------

**unittest**


Using ApiCheckerMixin::

    class TestAPIAgreements(ApiCheckerMixin, TestCase):
        def get_fixtures(self):
            return {'customer': CustomerFactory()}

        def test_customer_detail(self):
            url = reverse("customer-detail", args=[self.get_fixture('customer').pk])
            self.assertGET(url)


Using ApiCheckerBase metaclass


    class TestAPIIntervention(TestCase, metaclass=ApiCheckerBase):
        URLS = [
                reverse("intervention-list"),
                reverse("intervention-detail", args=[101]),
               ]

        def get_fixtures(cls):
            return {'intervention': InterventionFactory(id=101),
               'result': ResultFactory(),
               }

ApiCheckerBase can produce API test with minimum effort but it offers less flexibility
than ApiCheckerMixin.

**pytest**


pytest integration is provided by two helpers `frozenfixture` and `contract`::


    from django.urls import reverse
    from drf_api_checker.pytest import contract, frozenfixture


    @frozenfixture()
    def frozen_detail(db):
        from demo.factories import DetailFactory
        return DetailFactory()

    @contract()
    def test_url(frozen_detail):
        url = reverse("master-list")
        return url


Custom checks:
--------------

Sometimes it is not possible to check a field by value,  but exists anyway a mechanism 
to check the contract (ie. `timestamp` field - _ignore for this example tools like [freezegun](https://github.com/spulec/freezegun)_)

To handle these situations you can write custom `Recorder` with custom `asserters`:


    from drf_api_checker.recorder import Recorder

    class TimestampRecorder(Recorder):
    
        def assert_last_modify_date(self, response: Response, stored: Response, path: str):
            value = response['last_modify_date']
            assert datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

custom asserter is a method named `assert_<field_name>`, in case of nested serializers
you can have more specific asserter using `assert_<fk_field_name>_<field_name>`


Links
-----

|||
|--------------------|------------------------------------------------------------|
| Develop            | [![travis-png-d]][travis-l-d]|
| Master             | [![travis-png-m]][travis-l-m]|
| Project home page: | https://github.com/saxix/drf-api-checker                   |
| Issue tracker:     | https://github.com/saxix/drf-api-checker/issues?sort       |
| Download:          | http://pypi.python.org/pypi/drf-api-checker/               |
| Documentation:     | https://drf-api-checker.readthedocs.org/en/develop/         |



[travis-png-m]: https://secure.travis-ci.org/saxix/drf-api-checker.svg?branch=master
[travis-l-m]: https://travis-ci.org/saxix/drf-api-checker?branch=master

[travis-png-d]: https://secure.travis-ci.org/saxix/drf-api-checker.svg?branch=develop
[travis-l-d]: https://travis-ci.org/saxix/drf-api-checker?branch=develop

[rtd-badge]: https://readthedocs.org/projects/drf-api-checker/badge/?version=master&style=plastic
[rtd-link]: https://drf-api-checker.readthedocs.org/en/master/

[codecov-badge]: https://codecov.io/gh/saxix/drf-api-checker/branch/develop/graph/badge.svg
[codecov]: https://codecov.io/gh/saxix/drf-api-checker

[pypi-version]: https://img.shields.io/pypi/v/drf-api-checker.svg
[pypi]: https://pypi.org/project/drf-api-checker/
