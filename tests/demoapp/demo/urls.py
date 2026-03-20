from django.contrib import admin
from django.urls import re_path

from .api import (
    MasterCreatAPIView,
    MasterDeleteAPIView,
    MasterListAPIView,
    MasterRetrieveAPIView,
    MasterUpdateAPIView,
)

admin.autodiscover()

urlpatterns = (
    re_path(r"^master/list/", MasterListAPIView.as_view(), name="master-list"),
    re_path(
        r"^master/detail/(?P<pk>.*)/",
        MasterRetrieveAPIView.as_view(),
        name="master-detail",
    ),
    re_path(
        r"^master/update/(?P<pk>.*)/",
        MasterUpdateAPIView.as_view(),
        name="master-update",
    ),
    re_path(
        r"^master/delete/(?P<pk>.*)/",
        MasterDeleteAPIView.as_view(),
        name="master-delete",
    ),
    re_path(r"^master/create/", MasterCreatAPIView.as_view(), name="master-create"),
    re_path(r"^admin/", admin.site.urls),
)
