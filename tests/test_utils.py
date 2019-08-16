# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from io import BytesIO

import pytest
import pytz
from dateutil.utils import today
from rest_framework.response import Response

from drf_api_checker.fs import mktree
from drf_api_checker.utils import (
    _read, _write, dump_fixtures, load_fixtures, load_response, serialize_response
)


def test_mktree(tmpdir):
    target1 = f'{tmpdir}/aa/bb/cc'
    target2 = f'{tmpdir}/aa/bb/ee'
    file1 = f'{tmpdir}/file.txt'

    with open(file1, 'w') as f:
        f.write('aaa')

    mktree(target1)
    assert os.path.isdir(target1)

    mktree(target2)
    assert os.path.isdir(target2)

    mktree(target2)
    assert os.path.isdir(target2)
    with pytest.raises(OSError):
        mktree(file1)


def test_write_file(tmpdir):
    file1 = f'{tmpdir}/file.txt'
    _write(file1, b'content')


def test_write_buffer():
    _write(BytesIO(), b'content')


def test_write_error():
    with pytest.raises(ValueError):
        _write(22, b'content')


def test_read_buffer():
    assert _read(BytesIO(b'abc')) == b'abc'


def test_read_error():
    with pytest.raises(ValueError):
        _read(22)


def test_read_file(tmpdir):
    with open(f'{tmpdir}/f.txt', 'w') as f:
        f.write('aaa')
    assert _read(f'{tmpdir}/f.txt') == b'aaa'


def test_dump_fixtures_single(detail):
    stream = BytesIO()
    data = dump_fixtures({'d': detail}, stream)
    stream.seek(0)
    assert json.loads(stream.read())
    assert data['d']['master']['pk'] == detail.pk
    assert [e['pk'] for e in data['d']['deps']] == [detail.master.pk]


def test_dump_fixtures_multiple(details):
    d1, d2 = details
    stream = BytesIO()
    data = dump_fixtures({'d': details}, stream)
    stream.seek(0)
    assert json.loads(stream.read())
    assert [e['pk'] for e in data['d']['master']] == [d1.pk, d2.pk]
    assert [e['pk'] for e in data['d']['deps']] == [d1.master.pk, d2.master.pk]


def test_load_fixtures_single(detail):
    stream = BytesIO()
    dump_fixtures({'d': detail}, stream)
    stream.seek(0)
    assert load_fixtures(stream) == {'d': detail}


def test_load_fixtures_multiple(details):
    d1, d2 = details
    stream = BytesIO()
    dump_fixtures({'d': details}, stream)
    stream.seek(0)
    assert load_fixtures(stream) == {'d': list(details)}


def test_serialize_response():
    assert serialize_response(Response({'set': set(),
                                        'int': 1,
                                        'str': 'abc',
                                        'utc': datetime.utcnow().replace(tzinfo=pytz.utc),
                                        'now': datetime.now(),
                                        'date': today().date()}, status=200))


def test_load_response():
    response = Response({'set': set(),
                         'int': 1,
                         'str': 'abc',
                         'utc': datetime.utcnow().replace(tzinfo=pytz.utc),
                         'now': datetime.now(),
                         'date': today().date()}, status=200)
    r = load_response(BytesIO(serialize_response(response)))
    assert r.status_code == response.status_code
