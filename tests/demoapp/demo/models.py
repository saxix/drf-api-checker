# -*- coding: utf-8 -*-
import logging
from django.db import models

logger = logging.getLogger(__name__)


class Capability(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("id",)
        app_label = 'demo'


class Master(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

    capabilities = models.ManyToManyField(Capability)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
        app_label = 'demo'


class Detail(models.Model):
    name = models.CharField(max_length=100)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)
        app_label = 'demo'
