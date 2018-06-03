# -*- coding: utf-8 -*-
from itertools import chain

from django.db.models import ForeignKey, ManyToManyField


class ForeignKeysCollector(object):
    def __init__(self, using):
        self._visited = []
        super(ForeignKeysCollector, self).__init__()

    def _collect(self, objs):
        objects = []
        for obj in objs:
            if obj and obj not in self._visited:
                concrete_model = obj._meta.concrete_model
                obj = concrete_model.objects.get(pk=obj.pk)
                opts = obj._meta

                self._visited.append(obj)
                objects.append(obj)
                for field in chain(opts.fields, opts.local_many_to_many):
                    if isinstance(field, ManyToManyField):
                        target = getattr(obj, field.name).all()
                        objects.extend(self._collect(target))
                    elif isinstance(field, ForeignKey):
                        target = getattr(obj, field.name)
                        objects.extend(self._collect([target]))
        return objects

    def collect(self, obj):
        if not hasattr(obj, '__iter__'):
            obj = [obj]
        self._visited = []
        self.data = self._collect(obj)
        self.models = set([o.__class__ for o in self.data])
    #
    # def __str__(self):
    #     return mark_safe(self.data)
