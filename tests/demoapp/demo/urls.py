from django.conf.urls import url
from django.contrib import admin

from .api import (MasterCreatAPIView, MasterDeleteAPIView, MasterListAPIView,
                  MasterRetrieveAPIView, MasterUpdateAPIView)

admin.autodiscover()

urlpatterns = (
    url(r'^master/list/', MasterListAPIView.as_view(), name='master-list'),
    url(r'^master/detail/(?P<pk>.*)/', MasterRetrieveAPIView.as_view(), name='master-detail'),
    url(r'^master/update/(?P<pk>.*)/', MasterUpdateAPIView.as_view(), name='master-update'),
    url(r'^master/delete/(?P<pk>.*)/', MasterDeleteAPIView.as_view(), name='master-delete'),
    url(r'^master/create/', MasterCreatAPIView.as_view(), name='master-create'),
    url(r'^admin/', admin.site.urls),
)
