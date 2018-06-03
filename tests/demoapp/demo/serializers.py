from rest_framework import serializers
from .models import Master, Detail


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ('id', 'name', 'capabilities', 'timestamp')


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        exclude = ()
