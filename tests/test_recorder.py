# -*- coding: utf-8 -*-
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
