import pytest

from drf_api_checker.exceptions import FieldAddedError, FieldMissedError, FieldValueError
from drf_api_checker.recorder import Recorder


def test_field_missing():
    checker = Recorder('')
    with pytest.raises(FieldMissedError, match='Missing fields: `b`'):
        assert checker.compare(expected={'a': 1, 'b': 2},
                               response={'a': 1}, view='ViewSet')


def test_field_added():
    checker = Recorder('')
    with pytest.raises(FieldAddedError, match='New fields are: `b`'):
        assert checker.compare(expected={'a': 1},
                               response={'a': 1, 'b': 1}, view='ViewSet')


def test_field_different_format():
    checker = Recorder('')
    with pytest.raises(FieldValueError, match='expected: `11`'):
        assert checker.compare({'a': 1}, {'a': 11}, view='ViewSet')


def test_innner_dict():
    checker = Recorder('')
    with pytest.raises(FieldValueError, match=''):
        assert checker.compare({'a': 1, 'b': {'b1': 1}},
                               {'a': 1, 'b': {'b1': 22}}, view='ViewSet')


class R(Recorder):
    def get_single_record(self, response, expected):
        return response['results'][0], expected['results'][0]


def test_custom_response():
    checker = R('')
    assert checker.compare({"count": 1, "results": [{'a': 1, 'b': {'b1': 1}}]},
                           {"count": 1, "results": [{'a': 1, 'b': {'b1': 1}}]}, view='ViewSet')


def test_custom_response_error():
    checker = R('')
    with pytest.raises(FieldValueError, match='') as excinfo:

        assert checker.compare({"count": 1, "results": [{'a': 1, 'b': {'b1': 1}}]},
                               {"count": 1, "results": [{'a': 1, 'b': {'b1': 22}}]}, view='ViewSet')
    assert """
- expected: `22`
- received: `1`""" in str(excinfo.value)
