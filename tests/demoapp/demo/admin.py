# -*- coding: utf-8 -*-
from django.contrib.admin import ModelAdmin, register

from .models import Master


@register(Master)
class MasterAdmin(ModelAdmin):
    pass
