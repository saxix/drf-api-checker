from itertools import chain

from django.db.models import ForeignKey, ManyToManyField


class ForeignKeysCollector:
    def __init__(self, using):
        self._visited = []
        super().__init__()

    def _collect(self, objs):
        objects = []
        for obj in objs:
            if obj and obj not in self._visited:
                concrete_model = obj._meta.concrete_model
                model_obj = concrete_model.objects.get(pk=obj.pk)
                opts = model_obj._meta

                self._visited.append(model_obj)
                objects.append(model_obj)
                for field in chain(opts.fields, opts.local_many_to_many):
                    if isinstance(field, ManyToManyField):
                        target = getattr(model_obj, field.name).all()
                        objects.extend(self._collect(target))
                    elif isinstance(field, ForeignKey):
                        target = getattr(model_obj, field.name)
                        objects.extend(self._collect([target]))
        return objects

    def collect(self, obj):
        if not hasattr(obj, "__iter__"):
            obj = [obj]
        self._visited = []
        self.data = self._collect(obj)
        self.models = {o.__class__ for o in self.data}
