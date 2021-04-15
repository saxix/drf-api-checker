import calendar
import datetime
import json

from django.core import serializers as ser
from django.db import DEFAULT_DB_ALIAS

from .collector import ForeignKeysCollector


class ResponseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
            return millis
        # return json.JSONEncoder.default(self, obj)


def _write(dest, content):
    if isinstance(dest, str):
        open(dest, 'wb').write(content)
    elif hasattr(dest, 'write'):
        dest.write(content)
    else:
        raise ValueError(f"'dest' must be a filepath or file-like object. It is {type(dest)}")


def _read(source):
    if isinstance(source, str):
        return open(source, 'rb').read()
    elif hasattr(source, 'read'):
        return source.read()
    raise ValueError(f"'source' must be a filepath or file-like object. It is {type(source)}")


def dump_fixtures(fixtures, destination):
    data = {}
    j = ser.get_serializer('json')()

    for k, instances in fixtures.items():
        collector = ForeignKeysCollector(None)
        if isinstance(instances, (list, tuple)):
            data[k] = {'master': [],
                       'deps': []}
            for r in instances:
                collector.collect([r])
                ret = j.serialize(collector.data, use_natural_foreign_keys=False)
                data[k]['master'].append(json.loads(ret)[0])
                data[k]['deps'].extend(json.loads(ret)[1:])
        else:
            collector.collect([instances])
            ret = j.serialize(collector.data, use_natural_foreign_keys=False)
            data[k] = {'master': json.loads(ret)[0],
                       'deps': json.loads(ret)[1:]}

    _write(destination, json.dumps(data, indent=4, cls=ResponseEncoder).encode('utf8'))
    return data


def load_fixtures(file, ignorenonexistent=False, using=DEFAULT_DB_ALIAS):
    content = json.loads(_read(file))
    ret = {}
    for name, struct in content.items():
        master = struct['master']
        many = isinstance(master, (list, tuple))
        deps = struct['deps']
        if not many:
            master = [master]

        objects = ser.deserialize(
            'json', json.dumps(master + deps), using=using, ignorenonexistent=ignorenonexistent,
        )
        saved = []
        for obj in objects:
            # if router.allow_migrate_model(using, obj.object.__class__):
            obj.save(using=using)
            saved.append(obj.object)

        if many:
            ret[name] = list(saved[:len(master)])
        else:
            ret[name] = saved[0]
    return ret


def serialize_response(response):
    data = {'status_code': response.status_code,
            'headers': response._headers,
            'data': response.data,
            'content_type': response.content_type,
            }
    return json.dumps(data, indent=4, cls=ResponseEncoder).encode('utf8')


def load_response(file_or_stream):
    from rest_framework.response import Response

    c = json.loads(_read(file_or_stream))
    r = Response(c['data'],
                 status=c['status_code'],
                 content_type=c['content_type'])
    r._is_rendered = True
    r._headers = c['headers']
    return r
