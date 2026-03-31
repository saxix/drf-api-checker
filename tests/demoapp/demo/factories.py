import factory
from factory.django import DjangoModelFactory

from .models import Capability, Detail, Master


class CapabilityFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Name %03d" % n)

    class Meta:
        model = Capability


class MasterFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Name %03d" % n)
    alias = factory.Sequence(lambda n: "Alias %03d" % n)

    class Meta:
        model = Master

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
