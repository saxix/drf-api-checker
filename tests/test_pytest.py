from django.urls import reverse

from drf_api_checker.pytest import contract
from drf_api_checker.recorder import Recorder


class MyRecorder(Recorder):
    def assert_timestamp(self, response, stored, path):
        assert response


@contract(recorder_class=MyRecorder)
def test_url(frozen_detail):
    url = reverse("master-list")
    return url
