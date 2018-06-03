from django.conf.urls import url
from django.contrib import admin

from .api import MasterListAPIView, MasterRetrieveAPIView

admin.autodiscover()

urlpatterns = (
    url(r'^master/list/', MasterListAPIView.as_view(), name='master-list'),
    url(r'^master/detail/(?P<pk>.*)/', MasterRetrieveAPIView.as_view(), name='master-detail'),
    url(r'^admin/', admin.site.urls),
)
