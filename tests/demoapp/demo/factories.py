# -*- coding: utf-8 -*-
import factory
from factory import DjangoModelFactory

from .models import Capability, Detail, Master


class CapabilityFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Name %03d" % n)

    class Meta:
        model = Capability
        # django_get_or_create = ('id',)


class MasterFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Name %03d" % n)
    alias = factory.Sequence(lambda n: "Alias %03d" % n)

    class Meta:
        model = Master
        # django_get_or_create = ('id',)

    @factory.post_generation
    def capabilities(self, create, extracted, **kwargs):
        if not create:
            self.capabilities.add(CapabilityFactory())

        if extracted:
            for capability in extracted:
                self.capabilities.add(capability)


class DetailFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Name %03d" % n)
    master = factory.SubFactory(MasterFactory)

    class Meta:
        model = Detail
        # django_get_or_create = ('id',)
