# -*- coding: utf-8 -*-
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView

from .models import Master
from .serializers import MasterSerializer


class MasterListAPIView(ListCreateAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()


class MasterUpdateAPIView(UpdateAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()


class MasterCreatAPIView(CreateAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()


class MasterDeleteAPIView(DestroyAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()


class MasterRetrieveAPIView(RetrieveAPIView):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()
